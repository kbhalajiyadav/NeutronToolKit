# Scientific correctness and validation gates

This version is an analysis-framework prototype, not a calibrated ORNL reduction and not evidence that a particular structural model is correct.

## Physical interpretations that must be demonstrated

- Distinguish neutron bulk mixture SLD from *internal spatial contrast* among physically distinct phases or molecular subdomains. A three-component neat blend does not automatically contain two distinct segregated phases.
- An ~3 nm correlation corresponds to Q ~ 2*pi/30 Å ~ 0.21 Å^-1 and belongs within SANS, not conventional micron-scale USANS.
- A Teubner-Strey fit is not a default proof of bicontinuity or cholesteric morphology.
- Changing isotopic labels can change coherent contrast and incoherent background. A calculated SLD ratio cannot be equated to a validated peak-height ratio without a suitable structural correlation model and instrumental corrections.
- Deuteration does not guarantee invariant molecular packing, pitch, or transition temperature; test against independent controls.
- Distinguish slit-smeared USANS from pinhole-smeared SANS resolution; no made-up instrument resolution parameters.
- Do not treat 40 wt% of a molecule as necessarily a 0.40 phase volume fraction.
- Fit intensity only when error bars and background corrections are understood. Inspect normalized residuals and fit identifiability, not only chi-square.

## Software acceptance gates before scientific figures

1. Verify exact Q units, I units, dI and dQ semantics from the reduced files and reduction log.
2. Test numeric import against ORNL/SasView reference curves.
3. Compare no-smearing theory against SasView's own results for known models.
4. Add actual instrument resolution metadata and independent resolution test cases.
5. Recover known parameters from synthetic datasets with and without noise.
6. Fit H and D experiments with common structural hypotheses only if justified experimentally.
7. Record which observations are direct data, assumptions, or simulation predictions.
8. Commit code/config revisions and save analysis reports with SHA-256 of input curves.

## Current implemented gates

Strict numeric Q/column validation, dI/dQ positivity, file checksum, explicit density requirements, and a fixed-parameter model curve with no silently assumed smearing. More validation is needed before quantitative model selection.
