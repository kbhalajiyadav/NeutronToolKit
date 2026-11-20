"""Fixed-parameter SasView engine previews. No invented peak fits or smearing."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .files import load

def preview(config_path, data_path=None, outdir="outputs/models"):
    from sasmodels.direct_model import Iq
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    model, pars = config["model"], config["parameters"]
    measured = load(data_path) if data_path else None
    if measured is not None:
        q = measured.q
    else:
        qmin, qmax = float(config["qmin"]), float(config["qmax"])
        n = int(config.get("points", 160))
        if qmin <= 0 or qmax <= qmin or n < 5:
            raise ValueError("Require qmin>0, qmax>qmin, points>=5")
        q = np.geomspace(qmin, qmax, n)
    predicted = np.asarray(Iq(model, q, **pars), dtype=float)
    if predicted.shape != q.shape or not np.all(np.isfinite(predicted)) or np.any(predicted <= 0):
        raise ValueError("Model failed to return finite positive intensities")
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(q, predicted, label="fixed-parameter model: " + model)
    meta = {"model": model, "parameters": pars, "config": str(config_path),
            "resolution": "none; intentionally not guessed", "fit_optimized": False}
    if measured is not None:
        good = measured.intensity > 0
        ax.errorbar(q[good], measured.intensity[good],
                    yerr=None if measured.di is None else measured.di[good],
                    fmt=".", markersize=4, label=measured.path.stem)
        meta["data"] = str(measured.path)
        meta["data_sha256"] = measured.sha256()
        if measured.di is not None:
            residual = (measured.intensity-predicted)/measured.di
            meta["unfitted_chi2"] = float(np.dot(residual, residual))
            np.savetxt(out / "residuals.csv",
                       np.column_stack((q, measured.intensity, predicted, residual)),
                       delimiter=",", comments="",
                       header="q_A_inv,I_measured,I_theory,normalized_residual")
    ax.grid(True, which="both", alpha=0.25)
    ax.set(xlabel="Q (Å⁻¹)", ylabel="I(Q) (cm⁻¹)")
    ax.legend()
    fig.tight_layout()
    target = out/"model_overlay.png"
    fig.savefig(target, dpi=180)
    plt.close(fig)
    (out/"model_overlay.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return target
