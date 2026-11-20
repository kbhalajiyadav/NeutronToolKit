# NeutronToolKit

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kbhalajiyadav/NeutronToolKit/blob/main/notebooks/NeutronToolKit_Colab_Quickstart.ipynb)

**No WSL or administrator rights?** Open the badge in a browser to run the public example data, preview models, and explore deuteration designs in a temporary Google Colab session. The terminal file browser is replaced by notebook selection widgets. See [Colab guide](docs/colab.md).

A reproducible, Python-based toolkit for SANS and USANS **reduced-data analysis**, intended for handoff between lab computers and students.

**v0.3 scope:** interactive reduced 1D file browser, keyboard selection and filters, I(Q)/Kratky/Porod/Guinier plots, quality checks, coherent neutron SLD, mixture SLD, and fixed-parameter sasmodels model previews. This is not an ORNL raw-event reduction tool and does not yet do fitted structural inference.

## New lab laptop (Windows 11)

Follow the complete numbered procedure in [docs/setup-windows.md](docs/setup-windows.md). Install WSL2/Ubuntu, Docker Desktop with WSL integration, Git, and VS Code. Then run inside the Ubuntu terminal:

    sudo apt update && sudo apt install -y git
    mkdir -p ~/lab && cd ~/lab
    git clone https://github.com/kbhalajiyadav/NeutronToolKit.git
    cd NeutronToolKit
    docker compose build
    docker compose run --rm toolkit python -m neutrontoolkit doctor
    docker compose run --rm toolkit python -m pytest -q

## Launch the terminal file browser

    docker compose run --rm toolkit python -m neutrontoolkit browse data/examples

Keyboard:
- Arrow keys: move through files
- Space: select/deselect highlighted file
- A: select all visible files
- U: unselect all files
- /: filter by filename or path (press Enter to return)
- P: plot selected *visible* files and save PNG, SVG and JSON metadata to outputs/plots
- 1/2/3/4: I(Q), Kratky, Porod, Guinier view
- R: reload, Q: quit

In Docker/WSL, P generates figure files rather than forcing a GUI window inside the container. Open PNG/SVG from VS Code or JupyterLab. The terminal remains usable after plotting.

## Commands for reproducible analysis

    docker compose run --rm toolkit python -m neutrontoolkit qc data/examples/synthetic_iq.dat
    docker compose run --rm toolkit python -m neutrontoolkit plot data/examples/synthetic_iq.dat --kind iq
    docker compose run --rm toolkit python -m neutrontoolkit plot data/examples/synthetic_iq.dat --kind kratky
    docker compose run --rm toolkit python -m neutrontoolkit simulate config/example_sphere.json
    docker compose run --rm toolkit python -m neutrontoolkit sld C36H45D17O2 --density 0.99
    docker compose run --rm toolkit python -m neutrontoolkit mix-sld config/example_water_mixture.json

**Important:** example density 0.99 is not verified for your sample. Supply measured densities or clearly label every assumption.

To open the interactive notebook environment:

    docker compose up lab

Then visit the token-protected local URL in the terminal log (port 8888).

## Lab structure

- src/neutrontoolkit/: file IO, terminal browser, plots, contrast, model previews
- data/examples/: synthetic teaching curves
- data/reduced/: untracked experimental reduced data
- outputs/: untracked figures, model overlays and metadata
- config/: model inputs and isotope formulation templates
- docs/: setup, module reference, ORNL ecosystem, validation and roadmap
- tests/: regression tests
- environment.yml, Dockerfile, compose.yaml: portable scientific environment
- .devcontainer/: VS Code Dev Containers configuration
- .github/workflows/: automated tests

## Scientific boundaries

Only reduced **1D ASCII** data are supported in v0.1 (.dat, .txt, .csv, .iq), with numerical columns Q, I(Q), dI (optional), dQ (optional). Inputs must have positive increasing Q. Unsupported raw NeXus, NXcanSAS/CanSAS XML, 2D image and instrument-specific formats are not silently interpreted. They require a separate loader or reduction workflow.

Model preview is calculated with sasmodels using **user-supplied parameters** and explicitly no guessed instrumental smearing. A model curve drawn over data is not a fitted or validated model. See [docs/validation.md](docs/validation.md).

**Do not commit raw beamline files, unpublished sample data, ONCat tokens, passwords or credentials.** The output and reduced-data directories are gitignored by default.

For documentation of the real ORNL environment and commands see [docs/ornl.md](docs/ornl.md).


## v0.2: model guidance, fitting screens, and HPC preparation

Run these from the repository root (or prefix with 'docker compose run --rm toolkit'):

    python -m neutrontoolkit guide config/model_guidance_cholesteric.json
    python -m neutrontoolkit compare config/model_comparison_tutorial.json
    python -m neutrontoolkit plan-runs config/run_manifest_example.csv

- [Evidence-first model selection](docs/model-selection.md): Q range, resolution, competing hypotheses, weighted fits, AICc/BIC, residuals and limits.
- [ORNL inventory, autoreduction and HPC](docs/remote-hpc.md): read-only commands, ORNL tools, Slurm template and access cautions.
- scripts/ornl_inventory.sh is read-only and runs only where you are authorized.
- scripts/slurm_compare.sbatch is a portable template requiring cluster-specific validation.

These are exploratory screening capabilities. Full instrumental resolution validation, constrained H/D joint fitting, global optimization/Bumps posterior sampling, and raw-event reduction integrations remain future work. CI installation/test checks do not replace instrument-level scientific validation.

Environment note: environment.yml is a shared dependency specification, **not yet a fully frozen cross-platform lockfile**. A lockfile and versioned container image digest are required before declaring a final lab release reproducible byte-for-byte.


## v0.3 — Lab deployment strategy and isotope-design scenarios

NeutronToolKit wraps maintained scientific libraries rather than reimplementing their algorithms. New documents:

- [Architecture and ownership boundaries](docs/architecture.md)
- [Fresh Windows/WSL installation](docs/setup-fresh-laptop.md)
- [VCU Athena HPC profile and Slurm](docs/athena.md)
- [Site-selective deuteration calculation and limits](docs/deuteration-design.md)

New commands after building Docker:

    docker compose run --rm toolkit python -m neutrontoolkit contrast-sweep config/deuteration_design_example.json

The site file is [profiles/vcu-athena.yaml](profiles/vcu-athena.yaml). It is a *declarative profile*, not an automated SSH login or HPC submit function. The Slurm example is [scripts/vcu_athena_contrast.sbatch](scripts/vcu_athena_contrast.sbatch), requiring a validated container image and authorized cluster access.

The deuteration example uses **assumed H-state densities and unknown prices**. It reports SLD changes and a *conditional component-SLD variance proxy*, not a validated 3-nm peak-height improvement or real purchasing-cost ranking. Each configuration needs scientific and procurement validation.

GitHub CI validates scientific package installation and synthetic regression tests. Docker build, the Athena runtime and experimental resolution remain separately unverified. For a production lab release, create a Conda lockfile and versioned container digest.
