"""Calculate isotope-sensitive neutron SLD from explicit component densities."""
import json
from pathlib import Path
import numpy as np

def sld(formula, density):
    if not np.isfinite(density) or density <= 0:
        raise ValueError("Density must be explicitly provided and >0 g/cm3")
    import periodictable as pt
    return float(pt.neutron_sld(pt.formula(formula), density=density)[0])

def mixture(components):
    if not components:
        raise ValueError("No components")
    w = np.asarray([c["mass_fraction"] for c in components], dtype=float)
    rho = np.asarray([c["density_g_cm3"] for c in components], dtype=float)
    if not np.all(np.isfinite(w)) or np.any(w < 0) or abs(float(w.sum()) - 1) > 1e-6:
        raise ValueError("Mass fractions must sum to 1")
    if not np.all(np.isfinite(rho)) or np.any(rho <= 0):
        raise ValueError("All component densities must be supplied and >0")
    phi = w/rho
    phi = phi/phi.sum()
    values = np.asarray([sld(c["formula"], float(r)) for c, r in zip(components, rho)])
    return {
        "mix_coherent_sld_1e-6_A-2": float(phi @ values),
        "components": [{"formula": c["formula"], "volume_fraction": float(phi[i]),
                        "coherent_sld_1e-6_A-2": float(values[i])}
                       for i, c in enumerate(components)],
        "caveat": "Ideal volume additivity; not a measure of nano/micron-scale domain contrast",
    }

def from_json(path):
    return mixture(json.loads(Path(path).read_text(encoding="utf-8"))["components"])
