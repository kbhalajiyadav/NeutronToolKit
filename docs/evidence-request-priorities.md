# Minimum evidence request: what files actually unblock the decision?

**Purpose:** help a scientist obtain the few missing records that change whether a real fit is valid. Ask for source exports from the facility/lab, not guessed configuration settings. Keep unpublished data in an approved private location.

## Tier 0 — request first (directly unblocks scientifically credible fitting)

**1. Matching same-run reduced 1D and 2D products.** If a 2D map and a merged 1D curve differ in scale, request the 1D output from the **same sample scattering run and configuration** as the 2D map, including mask and binning details. Require actual Q/I/dI/dQ or Qx/Qy/I/dI/dQx/dQy columns/units.

**2. Reduction recipe and logs.** Facility-created drtSANS or Mantid input JSON/scripts and version; reduction log and metadata, sample/empty-cell/background, transmission, thickness, reference standard/absolute scale, normalization, masking, wavelength corrections, and the exact contributing run IDs. A run-list CSV does not replace these records.

**3. Configuration-specific reduced 1D curves** for each sample and configuration (include any long-wavelength repeat as separate original reduction). Request the per-configuration Q/I/dI/dQ, wavelength/distance, and run ID. Record if the later repeat was included in an existing merge.

**4. Resolution and merge semantics.** What is dQ? One-sigma, FWHM or other width? How do dQx/dQy map to instrument resolution? Which weighted stitching/interpolation/rebinning generated the merged Q points, and what uncertainty correlations exist? A dQ column is not a sufficient instrument resolution certification.

## Tier 1 — strongly improves 2D interpretation and structural hypotheses

**5. Corrected/background references in 2D** for the same configuration as the sample; blank/empty cell, transmission, detector masks, beam-center and geometry, and matching 2D outputs for other samples. Compare the same correction stages, not raw vs background-subtracted products.

**6. Sample and holder metadata:** aliquot/run mapping, exact formulation *by mass and/or mole*, cell thickness/path length and window material, sample transmission, measurement temperature, phase/visual observations, preparation history, orientation, shear/field conditions and any remounts.

**7. Independent physical constraints:** sample-specific density at measurement temperature (or documented uncertainty range), phase-transition data/DSC, polarized microscopy, SAXS/WAXS/XRD if available, pure-component/blank controls. These allow physical model eligibility or bounds; they are not mandatory for basic empirical peak characterization.

## Tier 2 — later or conditional

**8. Raw event NeXus files:** ask for these only if original reduced exports and recipes are missing or inconsistent and an authorized, validated re-reduction is required. They are large, access-controlled, and do not alone encode the final analyst choices.

**9. Deuteration feasibility inputs:** site-specific isotope enrichment and supplier data, sample-cell minimum volume, transmission/background/counting-time targets, available synthesis routes under approved lab procedures and verified costs. Request after the preliminary hypothesis/contrast matrix; do not assert a single minimum deuteration amount from SLD alone.

## File-to-decision mapping

| Desired decision | Minimum evidence needed |
| --- | --- |
| Describe measured 1D peak position | Existing reduced 1D Q/I/dI, documented fit range; provisional if reduction is unverified |
| Resolve 2D versus merged-1D intensity difference | Same-run 1D + 2D, exact reduction/corrections, masks and scale provenance |
| Apply resolution-corrected peak width | Per-configuration data, documented dQ/geometry and smearing convention |
| Compare physically eligible models across full Q | Original configuration reductions, properly treated background/absolute scale, parameter priors and uncertainty model |
| Infer alignment from 2D anisotropy | Matching blank/reference 2D, beam-center/masks, corrected 2D, sample orientation conditions |
| Compute molecule/region SLD | Verified structure, isotope abundance, temperature-relevant density/partial volumes |
| Estimate minimum feasible selective D labeling | Surviving model hypotheses, reliable count/background predictions, enriched-site composition, cell mass/geometry, feasibility and costs |

## Request format

Ask for an **approved private export folder** containing (a) sample-specific reduced 1D and corresponding 2D for each configuration; (b) the associated reduction JSON/scripts and logs; (c) same-config empty-cell/transmission/standard products; and (d) a note describing how repeats and overlapping curves were merged and how dQ is defined. A README naming which runs and processing versions are represented is particularly valuable.

Prefer the provenance-rich canSAS/NXcanSAS outputs when the facility can supply them, plus plain-text ASCII curves for independent numerical comparison. Do not upload restricted datasets to public repositories, public notebooks or unapproved AI services.
