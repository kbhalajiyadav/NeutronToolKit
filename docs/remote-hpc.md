# ORNL remote inventory, reduction, HPC

## Authorized remote inventory

Connect to https://analysis.sns.gov with your existing approved account. Review and run scripts/ornl_inventory.sh in your remote shell, or paste its read-only commands. This shows commands on PATH, Conda environments, Python packages and loaded modules. It does not search sample directories or print tokens.

The drtsans project documents three ORNL remote environments: sans (stable), sans-qa (testing), sans-dev (development). It also documents the drtsans wrapper command for an interactive scientific Python shell. Availability depends on the system/session.

## Reduction is distinct from modeling

EQSANS autoreduction can produce Iq.dat and Iq.png, 2D Iqxqy, JSON reduction parameters, HTML reports, HDF logs and GPR visualizations. It depends on metadata, beam center, empty beam, background, transmission, mask, calibration and normalization, not just filenames. GPR is nonparametric curve smoothing, NOT a physically identified structural model.

Dry-run matching only (no reduction):
    python -m neutrontoolkit plan-runs config/run_manifest_example.csv

Use ORNL drtsans/usansred/Mantid for validated raw-event reduction, with instrument scientist review.

## HPC deployment

ORNL remote desktop access does NOT guarantee Pathfinder/CADES HPC access. Verify separate allocation/approval, scheduler, partitions, permitted storage and software modules.

The repository contains scripts/slurm_compare.sbatch as a PORTABLE TEMPLATE only. It has no hard-coded account/partition and has not been tested on ORNL HPC. Confirm the documented Slurm environment-export rules for that specific system. Never run heavy fitting on shared login nodes. Prefer approved Apptainer/SIF on HPC rather than Docker daemon. Only pursue GPU support when a benchmark shows benefit.

Roadmap: local exploratory fits -> benchmark CPU/memory -> bounded model-screen batch runs -> multicontrast Bumps/DREAM -> HPC job arrays and versioned scientific result bundles.

References:
https://drtsans.readthedocs.io/latest/user/autoreduction.html
https://drtsans.readthedocs.io/latest/drtsans/reduction_scripts.html
https://github.com/neutrons/usansred
https://github.com/cw-do/eqsanscli
https://docs.cades.ornl.gov/pathfinder/pf-overview/
https://docs.cades.ornl.gov/pathfinder/pf-slurm/
https://docs.cades.ornl.gov/pathfinder/pf-python/
https://docs.cades.ornl.gov/pathfinder/pf-container/
