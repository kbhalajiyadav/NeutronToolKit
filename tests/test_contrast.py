import math
import pytest
from neutrontoolkit.contrast import sld, mixture

def test_isotopic_shift():
    h = sld("H2O", 1.0)
    d = sld("D2O", 1.1056)
    assert d > h

def test_mixture_mass_to_volume_fractions():
    result = mixture([{"formula":"H2O","mass_fraction":0.5,"density_g_cm3":1.0},
                      {"formula":"D2O","mass_fraction":0.5,"density_g_cm3":1.1056}])
    assert sum(c["volume_fraction"] for c in result["components"]) == pytest.approx(1.0)
    a,b = [c["coherent_sld_1e-6_A-2"] for c in result["components"]]
    assert a < result["mix_coherent_sld_1e-6_A-2"] < b

def test_invalid_weight():
    with pytest.raises(ValueError, match="sum to 1"):
        mixture([{"formula":"H2O","mass_fraction":0.2,"density_g_cm3":1.0}])

def test_missing_density():
    with pytest.raises((ValueError, TypeError)):
        mixture([{"formula":"H2O","mass_fraction":1.0,"density_g_cm3":None}])
