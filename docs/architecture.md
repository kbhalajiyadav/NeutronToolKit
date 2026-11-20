# NeutronToolKit as a scientific wrapper: maintenance strategy

## Ownership boundaries

NeutronToolKit owns the beginner-facing file browser, workflow recipes, input validation, reproducible orchestration, documentation and provenance. It does NOT reimplement Mantid reduction, sasmodels form factors, Bumps MCMC or PeriodicTable tabulations. This reduces the maintenance burden when upstream software changes.

| Operation | Preferred maintained backend | Local wrapper responsibility |
| --- | --- | --- |
| Raw EQ-SANS/GP-SANS/Bio-SANS reduction | ORNL drtsans / Mantid | Validated run manifest and config, provenance, permissions |
| USANS raw reduction | ORNL-approved USANS workflow | Data interface and metadata checks |
| 1D/2D reduced-data input | sasdata / suitable maintained readers | Validate units and source metadata |
| Structural models | sasmodels | Hypothesis eligibility, model recipes, bounded parameters |
| Parameter fitting | Bumps and SciPy | Diagnostics, consistent Q grids, uncertainty reporting |
| Isotopic SLD | PeriodicTable | Site-label scenario grid, mass-basis bookkeeping |
| Scheduling | Slurm, Apptainer | Site profiles and tested batch templates |
| Outputs | Matplotlib and JupyterLab | Accessible plots, structured reports, data hashes |

## Adapter design

Separate adapters per backend: sasmodels, periodictable, drtsans, Mantid, Slurm. Require clearly versioned inputs/outputs. Do not import optional heavy backends in the core file-browser path. Store instrument recipes under profiles/instruments once real metadata has been checked.

The VCU Athena YAML profile is descriptive in the first version; the corresponding Slurm template is explicit and **does not automatically connect or submit jobs**. This prevents undocumented credential handling.

## Upstream updates and validation

Lock major/minor versions for stable releases, run synthetic and reference-data regression tests against each dependency update, test model normalization and resolution, and publish validated container image digests. Keep large experimental data in approved lab storage, not Git. Let students choose guided workflows with an "advanced parameters" panel.

Begin with the local scientific pipeline. Add Athena when an approved account and image exist; add ORNL remote inventory and raw-event reduction only after access is restored.
