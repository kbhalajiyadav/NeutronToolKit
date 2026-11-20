# Full-curve model-selection protocol: physics before optimizer

**Status: scientific specification, not a certified fit.** Experimental data and derived numerical reports stay in approved private storage.

## Forward model and instrument gate

For every observation, evaluate instrument-smeared coherent scattering plus separately justified incoherent and residual backgrounds. Preserve sample thickness, transmission, absolute calibration, reduction log, uncertainties and original instrument configurations. A merged scattering curve can hide discontinuities in Q resolution and normalization: validate individual settings before imposing a single global fit.

**Neat mixtures:** Whole-molecule SLD does not define a scatterer/solvent boundary. In a multicomponent system the coherent intensity depends on partial spatial correlations, including cross terms: I(q) ~ sum_{ij} Delta_rho_i * Delta_rho_j * S_ij(q). An additive intensity model discards cross terms unless independent contributions are justified.

## Which parameters chemistry can and cannot supply

| Parameter | Source | Treatment |
|---|---|---|
| Molecular formula, isotope count, molar mass | Formula / PeriodicTable | Fixed if chemical identity verified |
| Coherent nuclear scattering lengths | PeriodicTable (NIST tables) | Fixed, versioned |
| Molecular volume | M/(density*N_A) | Conditional on measured density and temperature |
| Coherent SLD | Sum of bound coherent b / molecular volume | Calculated with density uncertainty |
| Mixture volume fractions | Mass fractions, each density, volume-additivity assumption | Calculated/qualified |
| Core/tail SLD | Fragment composition AND fragment partial volumes | Uncertain structural prior |
| Molecular shape/length | RDKit conformer ensemble, X-ray/MD corroboration | Prior, NOT exact from formula |
| Domain radius/shape, correlations, alignment | Independent imaging/scattering | Hypothesis or fitted parameter |
| Peak d-spacing | 2*pi/q0 from fitted peak | Empirical descriptor |
| Flat/incoherent background | Controls and chemistry | Nuisance, bounded |
| Q resolution | Beamline settings / reduction output | Must be confirmed |

Chemical formula cannot independently supply **bulk density, helix pitch, spatial organization, domain topology or exact molecular length**.

## Decision tree: single vs + vs @ vs custom

1. Begin with a **no-peak** baseline, **empirical** Lorentzian/Gaussian and native sasmodels broad_peak models. These test whether a peak is measurable but cannot identify a structural morphology.
2. Use one physical form-factor/correlation model only if independent structural evidence supports its geometry and it can describe all reliably measured Q.
3. Use **A+B** only for independently supported scattering processes/populations or a defensible scale separation. Confirm backgrounds counted only once and whether neglected cross terms matter.
4. Use **P@S** only for identifiable scattering objects AND interparticle correlations. Do not assign sphere@hardsphere solely because the ingredient list has three molecules.
5. Build a **custom SLD profile/correlation model** only when standard physical models cannot represent a specific, independently motivated arrangement; validate limiting cases, normalization and scattering contrast.
6. Do not default to Teubner-Strey without evidence of two actual distinct correlated phases, or lamellar models without independent layered-order evidence.

## Candidate fit sequence

A. Reproduce the original empirical peak fit and errors on the same Q, I and dI values. Track excluded points and hashes.

B. Test the low-Q power law over multiple prespecified Q intervals, the local broad-peak alternatives, and the reliable high-Q background. Do not interpret a numerically convenient polynomial as scattering physics.

C. Fit physical hypotheses using **native sasmodels DirectModel**, verified dQ/slit resolution and the same Q points/likelihood. Where physical evidence supports it, test joint fits across related samples with shared chemical priors and sample-specific structural parameters.

D. Use Bumps for bounded/constrained optimization, multistart, uncertainty and posterior sampling. Reject parameter degeneracy, boundary solutions and systematic residual structure. Report covariance/uncertainty assumptions, parameter profile stability, model-independent observables and Q-band/configuration holdout tests.

E. Use AICc/BIC only for models fitted to identical observations under a defensible error model. A lower AICc does not prove a structure. If all fits have large, structured residuals, state **NO MODEL ADEQUATE**.

## Release gate for a claimed physical model

A fit cannot be labeled "validated" unless it records: exact dataset and reduction provenance; Q/I/dI/dQ semantics and measured resolution; explicit structural assumptions; per-parameter origin and bounds; controls/absolute scale; residual and systematic-error checks; fit-window and multistart stability; independent/predictive checks; scientifically meaningful alternative models; and an inconclusive outcome when assumptions fail.

## Maintained upstream engines

- https://www.sasview.org/docs/dev/sasmodels-api/direct_model.html
- https://www.sasview.org/docs/dev/sasmodels-api/bumps_model.html
- https://www.sasview.org/docs/user/qtgui/Perspectives/Fitting/fitting_sq.html
- https://www.sasview.org/docs/user/qtgui/Perspectives/Fitting/resolution.html
- https://www.sasview.org/docs/user/qtgui/Calculators/sld_calculator_help.html
- https://periodictable.readthedocs.io/en/latest/api/nsf.html
- https://www.rdkit.org/docs/GettingStartedInPython.html

This public document contains **no experimental datasets or numerical sample-fitting results**. It is the qualification rulebook for the next validation implementation.
