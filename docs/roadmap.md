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
