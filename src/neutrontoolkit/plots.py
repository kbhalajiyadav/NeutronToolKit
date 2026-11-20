"""Plots of reduced experimental scattering data; not structural fits."""
from datetime import datetime, timezone
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .files import load

KINDS = ("iq", "kratky", "porod", "guinier")

def transform(curve, kind):
    q, y, di = curve.q, curve.intensity, curve.di
    if kind == "iq":
        return q, y, di, "Q (Å⁻¹)", "I(Q) (cm⁻¹)"
    if kind == "kratky":
        return q, q**2*y, None if di is None else q**2*di, "Q (Å⁻¹)", "Q² I(Q)"
    if kind == "porod":
        return q, q**4*y, None if di is None else q**4*di, "Q (Å⁻¹)", "Q⁴ I(Q)"
    if kind == "guinier":
        if np.any(y <= 0):
            raise ValueError("Guinier ln I requires strictly positive I(Q)")
        return q**2, np.log(y), None if di is None else di/y, "Q² (Å⁻²)", "ln I(Q)"
    raise ValueError("Plot types: iq, kratky, porod, guinier")

def plot_files(paths, kind="iq", outdir="outputs/plots"):
    curves = [load(path) for path in paths]
    if not curves:
        raise ValueError("No files selected")
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    for curve in curves:
        x, y, dy, xl, yl = transform(curve, kind)
        if kind == "iq":
            good = y > 0
            if not np.any(good):
                raise ValueError(f"No positive intensities for log plot: {curve.path}")
            x, y = x[good], y[good]
            if dy is not None:
                dy = dy[good]
        if dy is None:
            ax.plot(x, y, "o-", markersize=3, linewidth=1, label=curve.path.stem)
        else:
            ax.errorbar(x, y, yerr=dy, fmt="o-", markersize=2.5,
                        linewidth=1, capsize=1, label=curve.path.stem)
    ax.set(xlabel=xl, ylabel=yl, title=f"Neutron scattering: {kind}")
    if kind == "iq":
        ax.set(xscale="log", yscale="log")
    elif kind in ("kratky", "porod"):
        ax.set_xscale("log")
    ax.grid(True, alpha=0.25, which="both")
    ax.legend(fontsize=8)
    fig.tight_layout()
    name = f"{kind}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"
    png = out / (name + ".png")
    fig.savefig(png, dpi=180)
    fig.savefig(out / (name + ".svg"))
    plt.close(fig)
    (out / (name + ".json")).write_text(json.dumps({
        "kind": kind, "files": [str(c.path) for c in curves],
        "sha256": [c.sha256() for c in curves],
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "note": "No structural fitting and no instrument resolution correction",
    }, indent=2), encoding="utf-8")
    return png
