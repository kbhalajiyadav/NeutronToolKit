"""Scientific compatibility policy must retain default-safe missing evidence rules."""
import json
from pathlib import Path


def test_compatibility_policy_has_explicit_default_block():
    policy = json.loads(Path("config/validation-compatibility-policy.json").read_text())
    assert policy["default_if_provenance_missing"] == "blocked_for_quantitative_interchange"
    assert policy["policy_status"] == "scientific_specification_not_fully_implemented"
    rules = policy["rules"]
    keys = [r["id"] for r in rules]
    assert len(keys) == len(set(keys))
    required = {"2d_vs_1d","merged_vs_individual","resolution_semantics","di_vs_dq",
                "absolute_scale","anisotropy","sld_internal","peak_width",
                "deuteration_minimum","model_fit_vs_validation"}
    assert required.issubset(keys)
    assert all(r["default"] in ("blocked","review_required") for r in rules)
    assert all(isinstance(r["requires"],list) for r in rules)


def test_compatibility_policy_doc_references():
    doc = Path("docs/validation-compatibility.md").read_text()
    assert "1D" in doc and "2D" in doc and "dQ" in doc and "dI" in doc
    assert "Not implemented as automatic certification" in doc
    ai = Path("docs/evidence-assistant-architecture.md").read_text()
    assert "No AI deployment or fine-tuning" in ai
