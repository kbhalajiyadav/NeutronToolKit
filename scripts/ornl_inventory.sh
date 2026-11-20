#!/usr/bin/env bash
# Read-only inventory for an authorized ORNL remote session; no secrets printed.
set -u
printf '=== ORNL software inventory ===\n'
date -u '+UTC: %Y-%m-%d %H:%M:%S'
uname -srm
if [[ -r /etc/os-release ]]; then grep -E '^(NAME|VERSION_ID)=' /etc/os-release; fi
printf '\n=== Commands on current PATH ===\n'
for app in python python3 conda micromamba drtsans mantidworkbench sasview jupyter git docker apptainer singularity sbatch srun sinfo qstat; do
  printf '%-18s ' "$app"
  command -v "$app" || printf 'not found\n'
done
if command -v conda >/dev/null 2>&1; then printf '\n=== Conda environments ===\n'; conda env list; fi
if type module >/dev/null 2>&1; then printf '\n=== Loaded modules ===\n'; module list 2>&1; fi
if command -v python3 >/dev/null 2>&1; then
python3 - <<'PY'
from importlib import metadata
for name in ("mantid","drtsans","usansred","sasview","sasmodels","sasdata",
             "bumps","periodictable","numpy","scipy","matplotlib","h5py",
             "hdf5plugin","pandas","dask","distributed","lmfit","emcee","pyFAI","scipp"):
    try: version=metadata.version(name)
    except metadata.PackageNotFoundError: version="not installed in current Python"
    print(f"{name:20} {version}")
PY
fi
printf '\nNote: other environments may contain additional packages.\n'
