# Open scientific resource map for a data- and physics-grounded SAS rulebook

The toolkit must orchestrate maintained software instead of duplicating model kernels. The native SAS model metadata already include parameter names, units, defaults, hard limits, documentation categories and structure-factor status. Those metadata do not establish a physical sample-specific hypothesis.

## Primary dependencies

| Stage | Maintained resource | Provided | Still required |
|---|---|---|---|
| Chemical identity | PubChem PUG REST / verified SMILES or InChI | molecular structure, formula, identifiers | isomer/stereochemical confirmation and purity |
| Nuclear scattering | PeriodicTable | b-coherent, isotope masses, SLD given density | density, isotope content and uncertainty |
| Reference SLD | ORSO SLD database | SLD lookup/calculators | verify data applies at measurement temperature |
| Molecular conformation | RDKit ETKDG | 3D conformer ensembles and approximate dimensions | condensed-phase packing / independent structural evidence |
| Data ingestion | SasData | 1D/2D, canSAS and NXcanSAS | confirm Q, dI, dQ, detector settings, reduction |
| Model registry and kernels | sasmodels | list_models, load_model_info, parameter tables, DirectModel | *physical* model eligibility and independent priors |
| Optimization | Bumps | constrained/shared parameters, DREAM sampling, uncertainty | appropriate likelihood, identifiability and predictive validation |
| ORNL reduction | drtsans/Mantid/usansred | instrument JSON and reduction algorithms | instrument-approved calibration and metadata |
| Optional alternate analysis | McSAS3, SASfit | particle-size distributions and independent model comparisons | valid particle hypotheses / review, not default |
| Optional reflectometry | BornAgain/refnx | multilayer and GISANS interfaces | not a default for bulk EQ-SANS |
| Remote computing | Slurm/Apptainer | reproducible compute jobs | valid allocation, environment and data policy |

## Technical catalog versus physical rulebook

Technical catalog: extracted automatically from installed sasmodels.core.list_models('all') and sasmodels.core.load_model_info(name). Parameter properties: name, units, default, limits, type, description, shape/structure-factor metadata. No copied equations or manual parameter lists required.

Scientific evidence card: curated rules for the actual sample and instrument. Each card requires a hypothesis, supporting and disqualifying observations, feasible sample-specific parameter ranges, necessary Q/resolution, expected distinguishable features, alternative models and failure criteria. Inferred settings must carry their uncertainty and provenance. Start with 8-12 physically relevant models rather than annotate hundreds of unsupported options.

## Q cannot come from chemical formula alone

Instrument Q coverage is controlled by wavelength, scattering angle, geometry, beamstop, detector configuration, resolution and reduction quality. Q = 4*pi*sin(theta)/lambda, with 2*theta the total scattering angle. It must be imported from the actual measured/reduced data and metadata. A hypothesized structural spacing d suggests a target q = 2*pi/d, but formula alone does not establish a spacing or true measured q.

For the earlier EQ-SANS dataset, Q~0.003 to 1.5 A^-1 was measured, with a weak broad feature near 0.20 A^-1, which corresponds to an empirical d~3.14 nm. An optical pitch 300-450 nm would imply q~0.0014-0.0021 A^-1, below this particular merged range. Neither observation proves a unique molecular organization.

## How much is feasible?

Ready with libraries: formula/isotope mass, SLD with density, model/parameter discovery, 1D/2D standard formats, forward scattering simulations, constrained fitting, common diagnostics.

Moderate integration: versioned parameter provenance, density evidence, instrument-specific dQ, physical-eligibility cards, comparison on common q, multi-sample shared-parameter experiments, staged "inconclusive" outcomes.

Research-intensive: valid core-tail molecular SLD correlation models for neat cholesteric mixtures, experimental error covariance, full-resolution joint SANS+USANS, physical identifiability, robust inference from 2D anisotropy.

Generally not identifiable: unique condensed-phase structure, phase topology, packing and true model class from chemical formula plus one 1D scattering curve alone.

## Recommended implementation order

1. Extract installed sasmodels model catalog dynamically, including version; test against native library.
2. Read real data with SasData and verify reduction + q-resolution semantics.
3. Connect verified structure/chemical identity, PeriodicTable and experimentally qualified densities.
4. Add 8-12 curated evidence cards and physically constrained parameter policies.
5. Fit reference/alternative models via DirectModel and Bumps; use multistart, Q band tests, residuals and uncertainty.
6. Validate against three earlier reduced sample datasets and independent instrumental controls without publishing unpublished inputs.
7. Only then design H/D contrast experiments using structure models which survived validation.

## Documentation

https://www.sasview.org/docs/dev/sasmodels-api/core.html
https://www.sasview.org/docs/dev/sasmodels-api/modelinfo.html
https://www.sasview.org/docs/dev/sasmodels-api/direct_model.html
https://www.sasview.org/docs/dev/sasmodels-api/bumps_model.html
https://github.com/SasView/sasdata
https://periodictable.readthedocs.io/en/latest/api/nsf.html
https://slddb.reflectometry.org/
https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
https://www.rdkit.org/docs/GettingStartedInPython.html
https://drtsans.readthedocs.io/latest/drtsans/reduction_scripts.html
https://github.com/BAMresearch/McSAS
