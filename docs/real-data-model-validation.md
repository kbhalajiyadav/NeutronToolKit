# Model validation with real reduced data

This module reproduces and challenges an empirical peak fit before assigning a physical structure. It is not raw ORNL data reduction, a certified correlation length, or a structural morphology classifier.

## Use approved local reduced data

The scientific data and run logs are not part of this PUBLIC GitHub repository. Do not upload unpublished laboratory files, instrument logs, or credentials. Copy approved 1D ASCII files with Q, I, dI and optional dQ into the gitignored data/reduced folder.

    python -m neutrontoolkit validate-peaks data/reduced/sampleA.dat data/reduced/sampleB.dat --outdir outputs/model_validation

The output directory contains audit.json with input SHA256, model fits and fit-window sensitivities; empirical_model_residuals.png; and data-derived residual CSV. These outputs may themselves be unpublished and are gitignored.

## Models

The first validation gate checks no-peak quadratic, quadratic plus Lorentzian, and quadratic plus Gaussian on identical measured Q points. The legacy comparison uses Q=0.06–0.60 Angstrom^-1, weighted by the reported dI, with explicit listing of any excluded points (I>0, dI<0.5I). It reports reduced chi-square, AICc, lag-one standardized-residual correlation, peak spacing, and fit-range sensitivity. It also refits A*q^-alpha+B at several low-Q upper cutoffs.

A lower AICc is not evidence of a particular molecular morphology. The Lorentzian inverse-HWHM length is not automatically the physical correlation length. Strong residual autocorrelation, large reduced chi-square, arbitrary background choice or detector-merging artifacts stop any claim that formal covariance gives total uncertainty.

## Next: SasView engine validation

Use existing sasmodels peak_lorentz, gaussian_peak and broad_peak models as separately tested physical/empirical candidates, with their exact compiled library versions and reference tests. Note that broad_peak's documentation and source have had a reported inconsistency in 2026. Its empirical power-law-plus-peak formula does not prove lamellae or a cholesteric helix.

For repeated fitting, replace repeated convenience Iq calls with sasmodels.DirectModel and Bumps after verifying the reduction Q resolution. Confirm the meaning of dQ from the beamline; merged detector configurations can have discontinuities in resolution, for which SasView recommends careful comparison or fitting configurations separately.

Keep three length scales distinct: optical pitch hundreds of nm (below merged EQ-SANS Q coverage), local 3 nm peak near Q 0.2 Angstrom^-1, and possible 0.5 nm packing near the upper Q limit. Hold off on mechanism claims until background calibration, controls and 2D data support them.

Official documentation:
https://www.sasview.org/docs/user/models/peak_lorentz.html
https://www.sasview.org/docs/user/models/gaussian_peak.html
https://www.sasview.org/docs/user/models/broad_peak.html
https://www.sasview.org/docs/user/qtgui/Perspectives/Fitting/resolution.html
https://www.sasview.org/docs/dev/sasmodels-api/direct_model.html
