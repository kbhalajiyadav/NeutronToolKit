"""Synthetic and failure-mode regression tests of peak validation."""
import json
import numpy as np
import pytest
from neutrontoolkit.peak_validation import analyze, write_report


def synthetic(tmp_path):
    q=np.geomspace(0.003,1.4,230)
    y=1.75+0.3*q+0.15*q*q+0.075/(1+((q-0.205)*23)**2)
    di=np.full_like(q,0.002);dq=np.full_like(q,0.003)
    path=tmp_path/"synthetic.dat"
    np.savetxt(path,np.column_stack([q,y,di,dq]),fmt="%.17g")
    return path


def test_synthetic_peak_recovery(tmp_path):
    path=synthetic(tmp_path)
    report,traces=analyze(path)
    assert report["d_nm"]==pytest.approx(2*np.pi/0.205/10,rel=0.015)
    assert report["delta_aicc_null_minus_lorentz"]>100
    assert report["models"]["lorentz"]["reduced_chi2"]<0.05
    assert len(report["window_sensitivity"])>=3


def test_provenance_and_plot(tmp_path):
    path=synthetic(tmp_path)
    out=write_report([path],tmp_path/"out")
    doc=json.loads(out.read_text(encoding="utf-8"))
    assert len(doc["samples"])==1
    assert len(doc["samples"]["synthetic"]["file_sha256"])==64
    assert (out.parent/"empirical_model_residuals.png").is_file()


def test_reject_missing_uncertainty(tmp_path):
    q=np.geomspace(0.003,1.4,230)
    path=tmp_path/"without_di.dat"
    np.savetxt(path,np.column_stack([q,2+q]))
    with pytest.raises(ValueError,match="dI"):
        analyze(path)
