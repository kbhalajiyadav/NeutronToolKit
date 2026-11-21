# Data compatibility, validation limits and non-interchangeability rules

**Scope:** reduced neutron-scattering data, chemistry/SLD constraints and structural-model fitting. This is a scientific policy. A written rule does not imply the software already enforces it; the deterministic enforcement status is recorded separately. Do not publish confidential instrument files, experimental results, run manifests, private reports or supplier information in this public repository.

## Interpretation of statuses

- **COMPARABLE:** a documented, testable mapping establishes a common measurement basis with relevant uncertainties and provenance.
- **REVIEW REQUIRED:** comparison is allowed *only* as exploratory QA; retain labels and record differences without numerical pooling or parameter equivalence.
- **BLOCKED:** do not combine, equate or use to validate physical parameters until the named evidence is supplied.
- **INCONCLUSIVE:** explicitly report missing or contradictory evidence. Do not fabricate a normalization factor, resolution function, density, instrument file or structural conclusion.

Compatibility is contextual and question-specific. Two records may be usable for qualitative comparison but invalid for shared absolute-intensity fitting.

## Matrix of things that are NOT automatically interchangeable

| Products/parameters | Default | What would permit a quantitative comparison |
| --- | --- | --- |
| Raw detector/event NeXus and reduced scattering intensity | BLOCKED | Reduction algorithm and inputs, calibration, masks, normalization and uncertainty propagation; raw counts are not I in cm^-1 |
| 1D radially averaged I(Q) and independently reduced 2D I(Qx,Qy) | REVIEW REQUIRED | Same acquisition(s), corrections, masks, normalization and geometry; reproduce the beamline's weighted radial averaging with its uncertainty treatment |
| Single-configuration reduced 1D and multi-configuration merged 1D | REVIEW REQUIRED | Run-to-config mapping; overlap ranges; point origin and resolution; merge weights, scales and per-configuration reduction provenance |
| 1D/2D of different runs of nominally identical samples | BLOCKED for shared calibration/fit | Sample identity, preparation/state, time, temperature, thickness, transmission, configuration, reduction and replication plan |
| Two repeat runs from the same setting | REVIEW REQUIRED | Verify actual acquisition conditions and sample stability; establish whether counts or reduced intensities were summed/weighted and how uncertainty was propagated |
| Pin-hole resolution dQ, Cartesian dQx/dQy, slit ql/qw and wavelength spread | BLOCKED | Facility-defined meaning, units, 1-sigma/FWHM convention and corresponding smearing algorithm; never equate widths by column name |
| dI and dQ | BLOCKED | These represent uncertainty in measured intensity and resolution/uncertainty in Q, respectively; not substitutes |
| Same ASCII columns from different processing histories | REVIEW REQUIRED | Explicit versioned reduction lineage, background subtraction, transmission, thickness, calibration and binning |
| I(Q) labeled cm^-1 and validated absolute intensity | BLOCKED until calibration | Standard reference and applied scaling/correction chain with documented absolute normalization |
| Radial pixel average and beamline-produced 1D I(Q) | REVIEW REQUIRED | Correct pixel solid-angle, mask, event/variance weighting, binning and correction stage; naive unweighted pixel averaging is only a diagnostic |
| Q from a measured file and expected Q inferred from structural spacing | BLOCKED as substitutes | One is experimental coverage, the other a hypothesis prediction |
| Low-Q power-law exponent and a verified fractal/surface dimension | BLOCKED | Valid scaling interval, appropriate structure class, resolution and background controls, stable exponent |
| Peak location 2*pi/q0 and a unique layer spacing/molecular pitch | REVIEW REQUIRED | Reproducible peak and supported structural assignment; a single broad peak alone is not unique |
| Empirical peak inverse HWHM and physical correlation length | BLOCKED | Correct peak model, resolution convolution and independent evidence that the width-to-length relation is physically applicable |
| Whole-molecule SLD and core/tail/domain SLD contrast | BLOCKED | Verified molecular fragment composition **and** partial molecular volumes and spatial correlations; homogeneous molecular SLD cannot describe internal contrast alone |
| Weight fraction, molecular deuteration occupancy, and material mass/volume | BLOCKED | Explicit composition basis, enrichment, molecular masses (changed by isotopes), component densities, sample/cell geometry and mass balance |
| Calculated or assumed density and measured temperature-specific density | REVIEW REQUIRED | Source, uncertainty and phase/temperature applicability; never mark assumed density as measured |
| Optimizer convergence/low AICc and validated physical morphology | BLOCKED | Instrument/covariance checks, physically eligible model, identifiable parameters, robust residuals, independent predictions |
| Computational reproducibility and experimental correctness | BLOCKED as equivalence | Successful CI proves software execution on test fixtures, not facility reduction or the correct structural interpretation |

## 2D-specific interpretation limitations

- Masked pixels and NaN values must remain visible in QC and must not silently become zeros.
- Odd azimuthal harmonics, opposite-Q asymmetry or an intensity gradient are **instrument/data-quality screening signals**. A real scalar nuclear SLD normally gives even elastic coherent intensity under Q inversion; unusual odd contributions must first prompt geometry, detector, background, centering and processing review.
- Even second-harmonic anisotropy may support an orientation hypothesis **only after** instrumental anisotropy and background correction checks and suitable controls.
- 2D data from one distance/wavelength do not cover the entire Q domain of merged 1D measurements.

## Comparison key: provenance required for model fitting

For each measurement record keep:
- sample ID and aliquot/mount state, composition and preparation; temperature and field/shear/orientation conditions where relevant;
- facility, instrument, run ID(s), acquisition datetime, detector distance, wavelength/band, masks and geometry;
- processing pipeline name + version, recipe/config, reduction date, input event/run IDs, output SHA256;
- intensity/cell background, transmission, thickness, absolute scale and polarization corrections with their source files;
- Q, I, dI, dQ (or Qx,Qy,dQx,dQy) units and *semantics*; covariance or binning assumptions;
- 1D/2D generation and merge lineage, including repeat-run handling and overlap weighting;
- scientific model ID/version, Q mask, background, resolution algorithm, fitted parameters, priors and diagnostic failures.

Do not infer missing values from filenames or default instrument names. If a value is absent use UNKNOWN and let the intended analysis gate fail.

## What is and is not currently implemented

**Implemented in the existing toolkit:** numeric 1D ASCII loading, unit-independent numeric QC, optional dI/dQ presence checks, file SHA256, user-supplied resolution policy in the fitting screen, empirical residual summaries, and a heuristic flag for abrupt adjacent dQ changes.

**Not implemented as automatic certification:** experimental sample matching, facility-reduction equivalence, detector solid-angle corrections, statistically valid 2D-to-1D recomputation, uncertainty covariance recovery, merge lineage reconstruction, reference absolute-scale validation, automated physical-model acceptance or guaranteed AI-supported decisions.

This document establishes rules for future tests and feature acceptance; it is not a claim that all gates can currently be automatically evaluated.

## Current pilot lesson, generalized

When a separately reduced 2D product and an earlier merged 1D curve have different intensity levels, the immediate outcome is **REVIEW REQUIRED**. Do not multiply one by a fitted adjustment to force agreement and then declare that factor an experimental calibration. First recover a same-run 1D export and the two original reduction recipes.

The same applies to abrupt dQ changes near merge regions: flag and investigate, but do not assume an error or invent which detector setting supplied each point.

## Next developer checks

1. Add structured data-provenance metadata and exact run/config identifiers before a shared analysis.
2. Implement a deterministic compatibility gate per intended operation: overlay, quantitative combined fit, resolution correction, or physical parameter claim.
3. Fail closed on missing mandatory fields; output precisely which source files or settings would unblock each gate.
4. Test synthetic incompatible pairs (mismatched runs, resolution semantics, scale, sample state) and independently verified compatible cases.
5. Preserve public/private separation and record policy revisions with scientific review.

See the evidence request checklist, whole-curve protocol and original scientific validation notes for details.
