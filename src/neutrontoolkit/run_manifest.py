"""Conservative run-pairing plan; never executes neutron data reduction."""
from pathlib import Path
from collections import defaultdict
import csv
import json

REQUIRED = {"run_id", "instrument", "configuration", "sample_id", "role"}
ROLES = {"sample", "empty_beam", "transmission", "background"}

def plan(csv_path):
    target = Path(csv_path)
    with target.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not REQUIRED.issubset(set(reader.fieldnames)):
            raise ValueError(f"CSV requires: {sorted(REQUIRED)}")
        runs = list(reader)
    if not runs:
        raise ValueError("No runs in manifest")
    seen = set()
    groups = defaultdict(list)
    for row in runs:
        if any(not row.get(field, "").strip() for field in REQUIRED):
            raise ValueError("Missing required run metadata")
        if row["role"] not in ROLES:
            raise ValueError(f"Invalid role: {row['role']}")
        if not row["run_id"].isdigit() or row["run_id"] in seen:
            raise ValueError(f"Invalid or duplicated run: {row['run_id']}")
        seen.add(row["run_id"])
        groups[(row["instrument"], row["configuration"])].append(row)
    output = []
    for row in runs:
        if row["role"] != "sample":
            continue
        group = groups[(row["instrument"], row["configuration"])]
        empty = [x["run_id"] for x in group if x["role"] == "empty_beam"]
        transmission = [x["run_id"] for x in group if x["role"] == "transmission"
                        and x["sample_id"] == row["sample_id"]]
        background = [x["run_id"] for x in group if x["role"] == "background"]
        problems = []
        if len(empty) != 1: problems.append(f"Expected one empty beam, got {len(empty)}")
        if len(transmission) != 1: problems.append(f"Expected one sample transmission, got {len(transmission)}")
        if len(background) != 1: problems.append(f"Expected one background, got {len(background)}")
        output.append({
            "run_id": row["run_id"], "sample_id": row["sample_id"],
            "instrument": row["instrument"], "configuration": row["configuration"],
            "empty_beam_run": empty, "transmission_run": transmission,
            "background_run": background, "needs_review": problems,
            "status": "metadata_pairs_to_review" if not problems else "blocked_in_manifest",
        })
    return {"source": str(target), "type": "dry_run_only_no_reduction",
            "candidates": output,
            "warning": "Matching metadata is not sufficient to validate masks, transmission, beam center, instrument calibration or background equivalence."}

def write_plan(csv_path, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan(csv_path), indent=2), encoding="utf-8")
    return output
