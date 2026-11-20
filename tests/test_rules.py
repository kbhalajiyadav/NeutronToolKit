import pytest
from neutrontoolkit.model_rules import guidance
from neutrontoolkit.run_manifest import plan

def test_neat_not_two_phase_by_default():
    r = guidance({"instrument":"EQSANS","sample_state":"neat_bulk",
                  "observations":{"broad_peak_q_A_inv":0.2}})
    assert r["candidates"][0]["model"] == "broad_peak"
    assert r["candidates"][0]["d_A"] == pytest.approx(31.4159265, rel=1e-6)
    assert not any(c["model"] == "teubner_strey" for c in r["candidates"])

def test_two_phase_gate():
    r = guidance({"observations":{"independent_two_phase_evidence":True}})
    assert any(c["model"]=="teubner_strey" for c in r["candidates"])

def test_run_pairing():
    r = plan("config/run_manifest_example.csv")
    assert r["type"] == "dry_run_only_no_reduction"
    assert len(r["candidates"]) == 2
    assert all(c["status"] == "metadata_pairs_to_review" for c in r["candidates"])

def test_bad_q():
    with pytest.raises(ValueError):
        guidance({"observations":{"broad_peak_q_A_inv": -1}})
