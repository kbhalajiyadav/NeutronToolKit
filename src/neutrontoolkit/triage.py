"""Read-only scientific triage of reduced 1D neutron-scattering data.

This intentionally stops before model selection, raw reduction, or physical
parameter inference. The report is a structured, actionable end-user checklist,
not an experimental certification.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import math

import numpy as np
from .files import load, quality


def _provided(value):
    return value is not None and value != "" and value != "unknown"




def detect_dq_discontinuities(q, dq, ratio_threshold=1.75):
    """Screen abrupt adjacent changes in reported dQ; never assign instrument origin.

    This is a heuristic QA flag, not proof of bad data or an automatic
    configuration label. Even physically legitimate detector settings may differ.
    """
    if dq is None or len(q) < 2:
        return []
    positive = (dq[:-1] > 0) & (dq[1:] > 0)
    ratio = np.ones(len(dq)-1, dtype=float)
    ratio[positive] = np.maximum(dq[:-1][positive], dq[1:][positive]) / np.minimum(
        dq[:-1][positive], dq[1:][positive]
    )
    candidates = np.where(positive & (ratio > ratio_threshold))[0]
    return [
        {
            "q_before_A_inv": float(q[i]),
            "q_after_A_inv": float(q[i+1]),
            "dq_before_A_inv": float(dq[i]),
            "dq_after_A_inv": float(dq[i+1]),
            "change_factor": float(ratio[i]),
            "status": "requires_instrument_metadata_review",
        }
        for i in candidates[:30]
    ]

def analyze(paths, context=None):
    """Return QC, readiness and next actions without guessing facility metadata."""
    if context is None:
        context = {}
    if not isinstance(context, dict):
        raise ValueError("Context JSON must contain an object")
    resolution = context.get("resolution") or {}
    if not isinstance(resolution, dict):
        raise ValueError("Context resolution must contain an object")
    experiment = context.get("experiment") or {}
    if not isinstance(experiment, dict):
        raise ValueError("Context experiment must contain an object")

    instrument = context.get("instrument")
    reduction_source = context.get("reduction_log_or_report")
    mode = resolution.get("mode")
    source = resolution.get("source")
    semantics = resolution.get("dq_semantics")
    if mode not in (None, "unknown", "pinhole", "slit", "none"):
        raise ValueError("resolution.mode must be unknown, pinhole, slit, none or null")

    results = []
    for path in paths:
        curve = load(path)
        q_min, q_max = float(curve.q[0]), float(curve.q[-1])
        n = len(curve.q)
        notes = []
        actions = []
        has_uncertainties = curve.di is not None
        if not has_uncertainties:
            actions.append("Provide dI with documented statistical meaning before weighted fitting.")
        if not _provided(instrument):
            actions.append("Record the instrument and each acquisition configuration.")
        if not _provided(reduction_source):
            actions.append("Locate the original reduction report and background/transmission/calibration history.")
        if not _provided(experiment.get("temperature_C")):
            actions.append("Record temperature and phase/experimental conditions.")
        if curve.dq is None:
            notes.append("No fourth dQ column; resolution cannot be inferred from Q alone.")
        if mode in (None, "unknown"):
            actions.append("Identify the instrument-specific resolution function and its source.")
        elif mode == "pinhole":
            if curve.dq is None or semantics != "one_sigma_A_inv" or not _provided(source):
                actions.append("Validate per-point dQ, one-sigma units and the original pinhole resolution source.")
        elif mode == "slit":
            if not _provided(source) or not all(_provided(resolution.get(k)) for k in ("ql_A_inv", "qw_A_inv")):
                actions.append("Supply beamline-verified slit ql/qw and their resolution conventions.")
        elif mode == "none":
            notes.append("Resolution deliberately omitted; peak widths are exploratory, not instrument-corrected.")
            actions.append("Use verified instrumental resolution before quantitative structural conclusions.")
        dq_flags = detect_dq_discontinuities(curve.q, curve.dq)
        if dq_flags:
            notes.append(
                f"{len(dq_flags)} abrupt adjacent dQ changes flagged (factor >1.75). "
                "They may indicate differing resolution regimes; not evidence of an error by themselves."
            )
            actions.append(
                "Review instrument-configuration overlap, dQ semantics and the merge/reduction provenance "
                "before resolution-sensitive model fitting."
            )
        nonpositive = int(np.count_nonzero(curve.intensity <= 0))
        if nonpositive:
            notes.append(f"{nonpositive} intensities are nonpositive; log plots must flag rather than silently discard them.")
        if n < 15:
            notes.append("Sparse Q sampling; model complexity and peak identifiability need particular care.")
        good = curve.intensity > 0
        relative_uncertainty = (
            float(np.median(curve.di[good] / curve.intensity[good]))
            if curve.di is not None and np.any(good) else None
        )
        # These are reciprocal Q scales, NOT measured particle dimensions or
        # resolution-limited spatial dimensions.
        geometric_reciprocal_nm = {
            "2pi_over_q_max_nm": float(2 * math.pi / q_max / 10),
            "2pi_over_q_min_nm": float(2 * math.pi / q_min / 10),
        }
        if has_uncertainties and n >= 15:
            preliminary_stage = "empirical_screening_possible"
        else:
            preliminary_stage = "data_review_before_fitting"
        results.append({
            "input": str(curve.path),
            "quality": quality(curve),
            "q_decades": float(math.log10(q_max / q_min)),
            "reciprocal_q_window_not_structural_size": geometric_reciprocal_nm,
            "median_relative_dI_for_positive_I": relative_uncertainty,
            "dq_discontinuity_screening_flags": dq_flags,
            "dq_jump_ratio_threshold_heuristic": 1.75,
            "preliminary_stage": preliminary_stage,
            "measurement_validated": False,
            "physical_model_validated": False,
            "notes": notes,
            "required_next_actions": actions,
        })
    if not results:
        raise ValueError("Provide at least one reduced 1D ASCII file")
    return {
        "workflow": "neutron_end_user_first_pass",
        "purpose": "Explain what can and cannot be concluded, then identify next actions.",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "context_declared_by_user_not_independently_verified": context,
        "datasets": results,
        "global_warnings": [
            "Numeric file validity does not establish background, calibration or normalization quality.",
            "Q coverage is measured data coverage, not a formula-derived property.",
            "The reciprocal-Q window is NOT a claim of observable structure or unique size.",
            "Do not automatically select a physical model from molecular formula or empirical peak shape.",
            "No experimental files are transmitted to GitHub by this command.",
        ],
    }


def write_report(paths, context_path=None, outdir="outputs/triage"):
    if context_path is None:
        context = None
        context_hash = None
    else:
        path = Path(context_path)
        raw = path.read_bytes()
        context = json.loads(raw)
        context_hash = hashlib.sha256(raw).hexdigest()
    report = analyze(paths, context)
    report["context_file_sha256"] = context_hash
    target = Path(outdir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / "triage.json"
    json_path.write_text(json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")
    lines = [
        "# NeutronToolKit — first-pass scientific triage",
        "",
        "**Status: screening only. No physical model has been selected or validated.**",
        "",
    ]
    for sample in report["datasets"]:
        qc = sample["quality"]
        lines.extend([
            f"## {Path(sample['input']).name}",
            "",
            f"- Measured Q: {qc['q_min_A_inv']:.5g}–{qc['q_max_A_inv']:.5g} Å⁻¹ "
            f"({qc['points']} points).",
            f"- dI recorded: {'yes' if qc['has_dI'] else 'no'}; "
            f"dQ recorded: {'yes' if qc['has_dQ'] else 'no'}.",
            f"- Screening status: **{sample['preliminary_stage']}**.",
            "- Do not interpret the Q-to-length conversion as a validated structural size.",
            "",
        ])
        if sample["required_next_actions"]:
            lines.append("**Next actions:**")
            lines.extend(f"- {action}" for action in sample["required_next_actions"])
            lines.append("")
        if sample["notes"]:
            lines.append("**Observations and limits:**")
            lines.extend(f"- {note}" for note in sample["notes"])
            lines.append("")
    lines.extend(["**Conclusion:** QC does not validate instrument reduction or determine a physical scattering model.", ""])
    (target/"NEXT_STEPS.md").write_text("\n".join(lines), encoding="utf-8")
    return json_path
