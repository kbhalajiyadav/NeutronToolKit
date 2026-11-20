"""Reproducible weighted least-squares comparison of fixed hypotheses via sasmodels.

This is a *screening* implementation. Bumps posterior sampling and systematic-error
models are separate later validation steps, not silently claimed here.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import math
import re

import numpy as np
from scipy.optimize import least_squares

from .files import load


def _resolution(config, curve, mask):
    block = config.get("resolution")
    if not isinstance(block, dict):
        raise ValueError("Supply resolution with mode and source (never guess from instrument name)")
    mode = block.get("mode")
    if mode == "none":
        if not block.get("reason"):
            raise ValueError("Resolution 'none' needs an explicit reason")
        return {}, "none (user elected; see reason)"
    if mode == "pinhole":
        if curve.dq is None:
            raise ValueError("Pinhole requires per-Q dQ values; do not infer them")
        if block.get("dq_semantics") != "one_sigma_A_inv":
            raise ValueError("Confirm dQ is one-sigma A^-1 before pinhole smearing")
        if not block.get("source"):
            raise ValueError("Pinhole dQ source is required")
        return {"dq": np.asarray(curve.dq[mask], dtype=float)}, "pinhole"
    if mode == "slit":
        if not block.get("source"):
            raise ValueError("Slit resolution requires an instrument scientist/source reference")
        if "ql_A_inv" not in block or "qw_A_inv" not in block:
            raise ValueError("Provide measured ql_A_inv and qw_A_inv; don't substitute pinhole dQ")
        ql, qw = float(block["ql_A_inv"]), float(block["qw_A_inv"])
        if not math.isfinite(ql) or not math.isfinite(qw) or ql < 0 or qw < 0:
            raise ValueError("Slit ql/qw must be finite and >=0")
        return {"ql": ql, "qw": qw}, "slit"
    raise ValueError("resolution.mode must be none, pinhole, or slit")


def _spec(spec):
    if not isinstance(spec, dict):
        raise ValueError("Candidate must be an object")
    name = spec.get("name")
    model = spec.get("model")
    hypothesis = spec.get("hypothesis")
    if not all(isinstance(x, str) and x.strip() for x in (name, model, hypothesis)):
        raise ValueError("Every candidate needs name, model, and physical hypothesis")
    fixed = spec.get("fixed", {})
    free = spec.get("fit", {})
    if not isinstance(fixed, dict) or not isinstance(free, dict):
        raise ValueError("Candidate fixed and fit must be objects")
    if set(fixed).intersection(free):
        raise ValueError(f"{name}: parameter cannot be both fixed and free")
    if not free:
        raise ValueError(f"{name}: fit requires at least one adjustable parameter")
    lo, hi, start = [], [], []
    for param, setting in free.items():
        for field in ("initial", "min", "max"):
            if field not in setting:
                raise ValueError(f"{name}/{param}: supply {field}")
        a, b, c = float(setting["initial"]), float(setting["min"]), float(setting["max"])
        if not all(map(math.isfinite, (a, b, c))) or not b < a < c:
            raise ValueError(f"{name}/{param}: require finite min < initial < max")
        start.append(a)
        lo.append(b)
        hi.append(c)
    for param, value in fixed.items():
        if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
            raise ValueError(f"{name}/{param}: fixed value must be finite numeric")
    return name, model, hypothesis, fixed, list(free), np.array(start), np.array(lo), np.array(hi)


def _fit_one(spec, q, y, dy, kw_resolution, max_nfev):
    from sasmodels.direct_model import Iq
    name, model, hypothesis, fixed, keys, start, lo, hi = _spec(spec)
    k, n = len(keys), len(q)
    if n <= k + 1:
        raise ValueError(f"{name}: need n > k+1 for AICc (n={n}, k={k})")

    def theory(x):
        pars = dict(fixed)
        pars.update(zip(keys, map(float, x)))
        predicted = np.asarray(Iq(model, q, **kw_resolution, **pars), dtype=float)
        if predicted.shape != q.shape or not np.all(np.isfinite(predicted)):
            raise ValueError(f"{name}: nonfinite/incorrect model predictions")
        return predicted

    def residual(x):
        return (y - theory(x))/dy

    result = least_squares(residual, start, bounds=(lo, hi), method="trf",
                           max_nfev=max_nfev, x_scale="jac")
    pred = theory(result.x)
    resid = (y-pred)/dy
    chi2 = float(np.dot(resid, resid))
    aicc = float(chi2+2*k+2*k*(k+1)/(n-k-1))
    bic = float(chi2+k*np.log(n))
    near_edge = [
        key for key, value, lower, upper in zip(keys, result.x, lo, hi)
        if min((value-lower)/(upper-lower), (upper-value)/(upper-lower)) < 0.001
    ]
    auto = float(np.corrcoef(resid[:-1], resid[1:])[0,1]) if n > 4 and np.std(resid)>0 else None
    if auto is not None and not math.isfinite(auto):
        auto = None
    return {
        "name": name, "model": model, "hypothesis": hypothesis,
        "parameters": {**fixed, **dict(zip(keys, map(float, result.x)))},
        "free_parameters": k, "n": n, "chi2": chi2, "reduced_chi2": chi2/(n-k),
        "aicc": aicc, "bic": bic, "optimizer_success": bool(result.success),
        "optimizer_message": str(result.message), "nfev": int(result.nfev),
        "near_bounds": near_edge, "residual_lag1": auto,
        "_q": q, "_y": y, "_dy": dy, "_prediction": pred, "_residual": resid,
    }


def compare(config_path, outdir=None):
    path = Path(config_path).resolve()
    config = json.loads(path.read_text(encoding="utf-8"))
    input_path = (path.parent / config["data"]).resolve() if not Path(config["data"]).is_absolute() else Path(config["data"])
    curve = load(input_path)
    if curve.di is None:
        raise ValueError("Model ranking requires positive measured dI for every point")
    low, high = float(config["q_min_A_inv"]), float(config["q_max_A_inv"])
    if not np.isfinite(low) or not np.isfinite(high) or low <= 0 or high <= low:
        raise ValueError("Require 0 < q_min_A_inv < q_max_A_inv")
    if low < curve.q.min() or high > curve.q.max():
        raise ValueError("Chosen fit Q range must lie within measured Q; do not invent instrument bounds")
    mask = (curve.q >= low) & (curve.q <= high)
    q, y, dy = curve.q[mask], curve.intensity[mask], curve.di[mask]
    if len(q) < 8:
        raise ValueError("Need at least eight measured points in common fit Q range")
    kwargs, resolution = _resolution(config, curve, mask)
    candidates = config.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 2:
        raise ValueError("Supply at least two competing hypotheses in candidates")
    max_nfev = int(config.get("max_nfev", 200))
    if not 1 <= max_nfev <= 20000:
        raise ValueError("max_nfev must be between 1 and 20000")

    done, failed = [], []
    for spec in candidates:
        try:
            fit = _fit_one(spec, q, y, dy, kwargs, max_nfev)
            if fit["optimizer_success"]:
                done.append(fit)
            else:
                failed.append({"name": fit["name"], "problem": fit["optimizer_message"]})
        except (ValueError, TypeError, RuntimeError, KeyError) as exc:
            failed.append({"name": spec.get("name", "unnamed"), "problem": str(exc)})
    if not done:
        raise ValueError(f"All candidate optimizations failed: {failed}")
    done.sort(key=lambda item: item["aicc"])
    best_aicc = done[0]["aicc"]
    for item in done:
        item["delta_aicc"] = item["aicc"] - best_aicc

    report_dir = Path(outdir) if outdir else Path("outputs/fitting") / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    report_dir.mkdir(parents=True, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    good = y > 0
    ax.errorbar(q[good], y[good], yerr=dy[good], fmt=".", label="measured data", capsize=1)
    for item in done:
        pred = item["_prediction"]
        positive = pred > 0
        ax.plot(q[positive], pred[positive], label=f'{item["name"]}: ΔAICc {item["delta_aicc"]:.1f}')
    ax.set(xscale="log", yscale="log", xlabel="Q (Å⁻¹)", ylabel="I(Q) (cm⁻¹)")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(report_dir/"model_comparison.png", dpi=180)
    plt.close(fig)
    for i, item in enumerate(done):
        title = re.sub(r"[^A-Za-z0-9_.-]", "_", item["name"])[:45]
        np.savetxt(report_dir/f"residual_{i:02d}_{title}.csv",
                   np.column_stack([q, y, dy, item["_prediction"], item["_residual"]]),
                   header="q_A_inv,I_measured,dI,I_model,normalized_residual", delimiter=",", comments="")

    clean = [{key: val for key, val in item.items() if not key.startswith("_")} for item in done]
    result = {
        "status": "screening_only_not_physical_model_identification",
        "data_file": str(input_path), "sha256_data": curve.sha256(),
        "configuration_file": str(path), "sha256_config": sha256(path.read_bytes()).hexdigest(),
        "instrument": config.get("instrument", "unspecified"),
        "q_min_A_inv": low, "q_max_A_inv": high, "n_common": len(q),
        "resolution": resolution, "resolution_inputs": config["resolution"],
        "statistical_best_aicc": done[0]["name"], "candidates": clean, "failures": failed,
        "warnings": [
            "AICc/BIC assume independent Gaussian dI and identical Q points/errors for all models.",
            "Model evidence, residual structure, identifiability and reduction/systematic errors override a numerical rank.",
            "Model expressions (+) and (@) require independent physical justification.",
            "This implementation uses SciPy local least-squares; use Bumps/DREAM for posterior uncertainty in a later validation stage.",
        ],
    }
    (report_dir/"comparison.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return report_dir/"comparison.json"
