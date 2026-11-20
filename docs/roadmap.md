# Lab handoff roadmap

## Stage 1 — available as starter v0.1

Docker and Conda-compatible setup, GitHub automated checks, JupyterLab, synthetic input, terminal data browser, selectable files, filtering, figure outputs, QC, neutron coherent SLD and fixed-parameter sasmodels previews.

## Stage 2 — required before ORNL reanalysis

- Import actual reduced EQ-SANS / USANS format families with preserved metadata.
- Add validated 1D CanSAS/NXcanSAS file readers through sasdata.
- Verify ASCII column schemas, uncertainties and instrument-specific dQ conventions.
- Add model library with hypothesis-driven choice and real slit/pinhole resolution convolution.
- Implement constrained multi-contrast fits and uncertainty propagation via bumps.
- Add report generation with input dataset hash, git commit SHA and model assumptions.

## Stage 3 — optional integration with ORNL

Raw-event reduction via drtsans/Mantid as a separately versioned execution image or permitted remote service, and USANS reduction via the appropriate ORNL tool. Avoid attempting a complete Mantid stack inside the lightweight starter container until specific instruments, file formats, access rights and runtime dependencies have been confirmed.

## Stage 4 — student operation

One-command installation, training examples, command recipes per beamline, locked dependency versions, published Docker images with digests, data-management policy, code review and regression acceptance reports.

## Stage 2a — first model-screening implementation

A documented evidence-gated model guide, bounded weighted least-squares comparison of two or more sasmodels hypotheses on common measured Q, explicit optional pinhole or slit resolution settings, AICc/BIC/residual output, conservative run metadata matching, read-only ORNL software inventory and a generic Slurm job template. Scientific validation of resolution and fit behavior remains required.

## Stage 2b — wrapper-first + HPC profile + isotope-design prototype

Descriptive VCU Athena profile and an independent Apptainer/Slurm batch template. Site-selective nominal H/D isotope fractions, input ratio sweeps, actual labeled weight-percent bookkeeping and component-SLD variance screening using PeriodicTable. No actual vendor pricing, core-tail structural scattering, background prediction, automatic remote login or validated HPC deployment yet.
