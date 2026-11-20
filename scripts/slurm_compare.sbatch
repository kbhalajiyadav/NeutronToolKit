#!/usr/bin/env bash
#SBATCH --job-name=ntk-compare
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
# Populate NTK_REPO, NTK_PYTHON, NTK_CONFIG for an authorized Slurm account.
# No site-specific Slurm account or partition is assumed.
set -euo pipefail
: "${NTK_REPO:?Supply absolute repo path}"
: "${NTK_PYTHON:?Supply validated Python interpreter path}"
: "${NTK_CONFIG:?Supply comparison configuration path}"
cd "${NTK_REPO}"
export OPENBLAS_NUM_THREADS=2
export OMP_NUM_THREADS=2
"${NTK_PYTHON}" -m neutrontoolkit compare "${NTK_CONFIG}"
