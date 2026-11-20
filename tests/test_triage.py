"""End-user triage regression tests: never invent instrument or structure facts."""
import json
from pathlib import Path
import pytest
import numpy as np
from neutrontoolkit.triage import analyze, write_report


def test_example_gives_measured_q_and_explicit_unknowns():
    report = analyze(["data/examples/synthetic_iq.dat"])
    row = report["datasets"][0]
    assert row["quality"]["points"] == 11
    assert row["quality"]["has_dI"] and row["quality"]["has_dQ"]
    assert row["physical_model_validated"] is False
    assert any("instrument" in a.lower() for a in row["required_next_actions"])
    assert any("resolution" in a.lower() for a in row["required_next_actions"])
    assert row["preliminary_stage"] == "data_review_before_fitting"


def test_no_di_prevents_weighted_screening(tmp_path):
    sample = tmp_path/"reduced.dat"
    q = np.geomspace(0.003,0.3,20)
    np.savetxt(sample, np.column_stack([q, 1.0/(1+q)]))
    report = analyze([sample])
    assert report["datasets"][0]["quality"]["has_dI"] is False
    assert any("dI" in a for a in report["datasets"][0]["required_next_actions"])


def test_reports_are_private_file_outputs_with_actions(tmp_path):
    context_path = Path("config/triage_context_example.json")
    path = write_report(["data/examples/synthetic_iq.dat"],context_path,tmp_path/"triage")
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["context_file_sha256"]
    assert not result["datasets"][0]["measurement_validated"]
    document = (path.parent/"NEXT_STEPS.md").read_text(encoding="utf-8")
    assert "Next actions" in document and "inconclusive" not in document.lower()


def test_invalid_context_is_rejected():
    with pytest.raises(ValueError,match="object"):
        analyze(["data/examples/synthetic_iq.dat"],["not a mapping"])
