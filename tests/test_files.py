import numpy as np
import pytest
from neutrontoolkit.files import load, discover, quality

def test_example():
    curve = load("data/examples/synthetic_iq.dat")
    assert len(curve.q) == 11
    assert curve.q[0] > 0
    assert curve.di is not None and curve.dq is not None
    assert quality(curve)["nonpositive_intensity"] == 0
    assert len(curve.sha256()) == 64

def test_reject_out_of_order_q(tmp_path):
    target = tmp_path / "x.dat"
    target.write_text("0.2 1 0.1\n0.1 2 0.1\n")
    with pytest.raises(ValueError, match="Q must"):
        load(target)

def test_reject_wrong_uncertainty(tmp_path):
    target = tmp_path / "x.dat"
    target.write_text("0.1 1 -0.1\n0.2 2 0.1\n")
    with pytest.raises(ValueError, match="dI"):
        load(target)

def test_discovery():
    assert any(p.name == "synthetic_iq.dat" for p in discover("data/examples"))
