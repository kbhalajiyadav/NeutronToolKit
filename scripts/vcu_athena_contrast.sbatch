#!/usr/bin/env bash
#SBATCH --job-name=ntk-contrast
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:30:00
# Requires an approved Athena account and a validated container image.
set -euo pipefail
test -d "$NTK_REPO" || { echo "Set NTK_REPO to existing Athena checkout" >&2; exit 2; }
test -f "$NTK_IMAGE" || { echo "Set NTK_IMAGE to validated .sif file" >&2; exit 2; }
test -f "$NTK_REPO/$NTK_CONFIG" || { echo "Set NTK_CONFIG to repo-relative JSON" >&2; exit 2; }
module load apptainer
cd "$NTK_REPO"
export OMP_NUM_THREADS=2
export OPENBLAS_NUM_THREADS=2
apptainer exec --cleanenv --bind "$NTK_REPO:/workspace" --pwd /workspace "$NTK_IMAGE" \
    python -m neutrontoolkit contrast-sweep "$NTK_CONFIG"
