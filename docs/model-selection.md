# NeutronToolKit model-selection rulebook (v0.2)

This is a hypothesis-screening framework, not an automatic physical structure classifier. Chemical formulas and bulk coherent SLD alone cannot determine spatial SLD correlations.

## Evidence gates

| Independent observation | Candidate model | Condition |
| --- | --- | --- |
| Smooth power-law intensity | power_law | Exponent is descriptive, not a unique topology |
| Broad SANS q~0.2 A^-1 peak | broad_peak | Empirical peak position/width, NOT proof of layers |
| Higher Bragg orders and microscopy-supported layering | lamellar_stack_paracrystal | Layered hypothesis and disorder bounds justified |
| Microscopy-confirmed droplets | sphere or core_shell_sphere | Droplet morphology and dispersion measured |
| Independently demonstrated two-phase correlations | teubner_strey | Two actual phases, not just multiple ingredients |
| Correlated particles | Form factor @ structure factor | Interparticle structure factor justified |
| Independent scattering populations | Model1 + Model2 | Scattering additions physically independent; no background double count |
| Strong anisotropic detector patterns | 2D models | 1D averaging loses orientation |

For a neat COC/CP/CC mixture, do not assume components are distinct domains, or equate mass fraction to phase volume fraction. At q=0.20 A^-1, 2*pi/q=31.4 A = 3.14 nm, a SANS rather than conventional micron-scale USANS feature.

## Commands

    python -m neutrontoolkit guide config/model_guidance_cholesteric.json
    python -m neutrontoolkit compare config/model_comparison_tutorial.json

Comparison uses sasmodels Iq and SciPy bounded least-squares and saves overlay PNG, residual CSVs and JSON report. It needs the same Q points, measured positive dI, a Q fit interval inside the actual data and explicit resolution parameters for all candidates.

Resolution modes:
- none: requires written reason; suitable only for teaching or explicitly acknowledged exploratory analysis
- pinhole: requires a dQ column whose meaning is confirmed as one-sigma in A^-1 and an identified source
- slit: requires actual ql and qw values from beamline documentation, never guessed from instrument name

On identical observations with independent Gaussian dI:
chi2 = sum(((Iobs-Imodel)/dI)^2).
AICc = chi2 + 2*k + 2*k*(k+1)/(n-k-1).
BIC = chi2 + k*ln(n).
k is number of fitted parameters; AICc needs n>k+1.

The best AICc is a statistical screening result only. Inspect systematic residual trends, bound hits, model identifiability, uncertainties, instrument resolution and baseline calibration. Abstain if independent physical evidence is absent.

Model expressions follow sasmodels semantics: plus denotes intensity sums of independent contributions; at-sign denotes P(Q)*S(Q) where valid. Combined model parameter names can differ from the component names. Custom plugin Python must be source-reviewed and tested, not loaded blindly.

Not implemented in v0.2: validated joint H/D constrained fitting, posterior DREAM/MCMC, automatic resolution metadata import, synthetic recovery across instrument profiles, 2D orientational analysis, or robust multistart global optimization.

Sources:
https://www.sasview.org/docs/dev/sasmodels-api/direct_model.html
https://www.sasview.org/docs/dev/sasmodels-api/bumps_model.html
https://www.sasview.org/docs/user/models/broad_peak.html
https://www.sasview.org/docs/user/models/teubner_strey.html
https://www.sasview.org/docs/user/qtgui/Perspectives/Fitting/plugin.html
