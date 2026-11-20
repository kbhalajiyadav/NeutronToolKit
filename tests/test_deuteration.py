import json
import math
import pytest
from neutrontoolkit.deuteration import sweep, write_sweep

def test_isotope_sweep_known_components():
    config=json.loads(open("config/deuteration_design_example.json",encoding="utf-8").read())
    result=sweep(config)
    assert len(result["summaries"]) == 4
    assert len(result["all_scenarios"]) == 4*3*4*3*4*3
    base=[x for x in result["all_scenarios"]
          if x["composition"]=="reference_20_40_40"
          and x["D_atom_mol_per_reference_batch"] == 0]
    assert len(base)==1
    active=max(
        (x for x in result["all_scenarios"] if x["composition"]=="reference_20_40_40"),
        key=lambda r:r["component_variance_proxy"])
    assert active["component_variance_proxy"] > base[0]["component_variance_proxy"]
    assert active["incremental_label_cost_usd_per_reference_batch"] is None
    assert all(not summary["actual_cost_ranking_available"] for summary in result["summaries"])
    for scenario in result["all_scenarios"]:
        assert sum(scenario["component_volume_fractions"].values()) == pytest.approx(1)
        assert sum(scenario["labeled_actual_mass_fractions"].values()) == pytest.approx(1)

def test_export(tmp_path):
    f=write_sweep("config/deuteration_design_example.json",tmp_path)
    assert f.is_file()
    assert (tmp_path/"all_scenarios.csv").is_file()

def test_reject_missing_density():
    config=json.loads(open("config/deuteration_design_example.json",encoding="utf-8").read())
    config["components"][0]["density_H_g_cm3"]=None
    with pytest.raises(ValueError,match="density"):
        sweep(config)
