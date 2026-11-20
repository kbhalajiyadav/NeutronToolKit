"""Evidence-gated guidance: recommend testable models, never identify structure from formula."""
import json
import math
from pathlib import Path

def guidance(payload):
    state = payload.get("sample_state", "unknown")
    if state not in {"neat_bulk", "dispersed_droplets", "aligned_lamellae", "unknown"}:
        raise ValueError("sample_state must be neat_bulk, dispersed_droplets, aligned_lamellae, or unknown")
    obs = payload.get("observations", {})
    instrument = payload.get("instrument", "unknown")
    candidates = []
    cautions = [
        "Model suggestions are hypotheses, not proof of morphology.",
        "Chemical formula or bulk SLD cannot determine the spatial correlation function or domain topology.",
        "Instrument resolution and reduction provenance are required before quantitative model ranking.",
    ]
    peak = obs.get("broad_peak_q_A_inv")
    if peak is not None:
        peak = float(peak)
        if not math.isfinite(peak) or peak <= 0:
            raise ValueError("broad_peak_q_A_inv must be positive")
        candidates.append({"model": "broad_peak", "priority": "baseline",
                           "role": "empirical peak position and width, not proof of lamellae",
                           "d_A": 2*math.pi/peak})
    else:
        candidates.append({"model": "power_law", "priority": "baseline",
                           "role": "model-free low-q decay reference"})
    if obs.get("independent_two_phase_evidence") is True:
        candidates.append({"model": "teubner_strey", "priority": "conditional",
                           "role": "two-phase correlation hypothesis: requires physical evidence of two phases"})
    else:
        cautions.append("Do not label teubner_strey as a default neat-cholesteric morphology.")
    if state == "dispersed_droplets" and obs.get("microscopy_confirms_droplets") is True:
        candidates.append({"model": "sphere", "priority": "conditional",
                           "role": "droplet form-factor hypothesis; verify size distribution and interactions"})
    if state == "aligned_lamellae" and obs.get("higher_order_bragg_peaks") is True:
        candidates.append({"model": "lamellar_stack_paracrystal", "priority": "conditional",
                           "role": "layered structure hypothesis supported by higher-order correlations"})
    if obs.get("anisotropic_2d") is True:
        cautions.append("Do not infer orientation from azimuthally averaged 1D curves alone; analyze 2D intensity.")
    if peak is not None and str(instrument).upper() == "USANS" and peak > 0.01:
        cautions.append("High-q peak lies outside typical USANS sensitivity; confirm actual instrument Q coverage.")
    if not obs:
        cautions.append("No observations supplied; only a baseline empirical model can be proposed.")
    return {
        "instrument": instrument, "sample_state": state,
        "candidates": candidates, "cautions": cautions,
        "decision": "Candidates require independent evidence and fitted residual checks; no automatic best physical model."
    }

def from_file(path):
    return guidance(json.loads(Path(path).read_text(encoding="utf-8")))
