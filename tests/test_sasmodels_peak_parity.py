"""Check empirical peak kernels against native SasView/sasmodels implementations."""
import numpy as np
from sasmodels.direct_model import Iq
from neutrontoolkit.peak_validation import lorentz, gaussian


def test_sasmodels_peak_lorentz_parity():
    q = np.linspace(0.08, 0.45, 120)
    amplitude, q0, hwhm = 0.082, 0.203, 0.046
    native = np.asarray(Iq("peak_lorentz", q, scale=amplitude,
                           background=0.0, peak_pos=q0, peak_hwhm=hwhm))
    empirical = lorentz(q, 0, 0, 0, amplitude, q0, 1.0/hwhm)
    np.testing.assert_allclose(native, empirical, rtol=2e-5, atol=1e-8)


def test_sasmodels_gaussian_peak_parity():
    q = np.linspace(0.08, 0.45, 120)
    amplitude, q0, sigma = 0.064, 0.208, 0.05
    native = np.asarray(Iq("gaussian_peak", q, scale=amplitude,
                           background=0.0, peak_pos=q0, sigma=sigma))
    empirical = gaussian(q, 0, 0, 0, amplitude, q0, sigma)
    np.testing.assert_allclose(native, empirical, rtol=2e-5, atol=1e-8)
