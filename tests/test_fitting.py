import json
import numpy as np
import pytest
from sasmodels.direct_model import Iq
from neutrontoolkit.fitting import compare

def test_recovers_known_synthetic_exponent(tmp_path):
    q = np.geomspace(0.01, 0.20, 21)
    y = np.asarray(Iq("power_law", q, scale=0.003, power=2.0, background=0.1))
    dI = np.full_like(q, 0.02)
    data = tmp_path/"synthetic.dat"
    np.savetxt(data, np.column_stack([q,y,dI]), fmt="%.17g")
    hypotheses = []
    for exponent in (2.0,4.0):
        hypotheses.append({"name":f"power_{exponent}", "model":"power_law",
          "hypothesis":"Synthetic known-exponent regression test",
          "fixed":{"power":exponent},
          "fit":{"scale":{"initial":0.001,"min":1e-10,"max":0.01},
                 "background":{"initial":0.2,"min":1e-6,"max":1.0}}})
    cfg = tmp_path/"fit.json"
    cfg.write_text(json.dumps({"instrument":"SYNTHETIC","data":str(data),
      "q_min_A_inv":float(q[0]),"q_max_A_inv":float(q[-1]),
      "resolution":{"mode":"none","reason":"Pure synthetic test"},
      "candidates":hypotheses,"max_nfev":150}))
    report = json.loads(compare(cfg, tmp_path/"results").read_text())
    assert report["statistical_best_aicc"] == "power_2.0"
    assert report["n_common"] == 21
    assert (tmp_path/"results"/"model_comparison.png").is_file()

def test_reject_resolution_unknown(tmp_path):
    q=np.geomspace(0.01,0.2,10)
    dat=tmp_path/"data.dat"
    np.savetxt(dat,np.column_stack([q,np.ones(10),np.full(10,0.1)]),fmt="%.17g")
    cfg=tmp_path/"fit.json"
    cfg.write_text(json.dumps({"data":str(dat),"q_min_A_inv":float(q[0]),
       "q_max_A_inv":float(q[-1]),"candidates":[{},{}]}))
    with pytest.raises(ValueError,match="resolution"):
        compare(cfg)
