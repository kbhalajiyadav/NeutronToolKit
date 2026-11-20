# Fresh Windows lab laptop: beginner installation (November 2026)

You should NOT install the neutron scientific packages individually on Windows. Use a WSL2 Linux Ubuntu development shell and Docker Desktop with WSL integration. Confirm the laptop is running Windows 11 and that lab IT permits installs.

## A. Windows preparation

1. Open Windows PowerShell as Administrator.
2. Check status:

    wsl --status
    wsl --list --verbose

3. If there is no Ubuntu distribution, install:

    wsl --install -d Ubuntu

4. Restart Windows if prompted. Open Ubuntu from Windows Start. Create a Linux username/password.
5. Install Docker Desktop (Linux containers / WSL2 backend) from the official Docker site. In Settings > Resources > WSL Integration, toggle the correct Ubuntu distribution ON. Start Docker Desktop.
6. Install VS Code and the WSL and Dev Containers extensions from official Microsoft extensions. Optional Windows Git is not required if you use Git in Ubuntu.

Official docs:
- https://learn.microsoft.com/en-us/windows/wsl/install
- https://docs.docker.com/desktop/setup/install/windows-install/
- https://code.visualstudio.com/docs/remote/wsl
- https://code.visualstudio.com/docs/devcontainers/containers

## B. Ubuntu / WSL

Open the Ubuntu terminal (NOT Windows PowerShell):

    sudo apt update
    sudo apt install -y git ca-certificates
    mkdir -p ~/lab
    cd ~/lab
    git clone https://github.com/kbhalajiyadav/NeutronToolKit.git
    cd NeutronToolKit
    pwd
    docker version
    docker compose version

Expected pwd begins /home/<linuxusername>/lab/NeutronToolKit. The Docker commands should find Docker Desktop. If not, open Docker Desktop and check Ubuntu integration; do not install another Docker engine into WSL.

## C. Build and test scientific runtime

    docker compose build
    docker compose run --rm toolkit python -m neutrontoolkit doctor
    docker compose run --rm toolkit python -m pytest -q

Wait for the commands to finish and read their output. If build/test fails, copy the error and check GitHub Actions. Do not interpret numerical results before tests pass.

## D. First plots and isotope scenarios

    docker compose run --rm toolkit python -m neutrontoolkit browse data/examples
    docker compose run --rm toolkit python -m neutrontoolkit contrast-sweep config/deuteration_design_example.json
    docker compose run --rm toolkit python -m neutrontoolkit guide config/model_guidance_cholesteric.json

In the terminal browser press Space to select an example data file and P to create PNG/SVG figures. They appear under outputs/plots; no GUI window is automatically opened from Docker. New isotope tables appear under outputs/deuteration.

To open VS Code from WSL:
    code .

## E. Jupyter

    docker compose up lab

Visit the token-protected localhost URL printed by JupyterLab. Press Ctrl+C in Ubuntu to stop it. Never disable the token or expose Jupyter to public networks.

## F. Install real data later

Put the reduced 1D Q, I(Q), dI, dQ ASCII files in data/reduced. This directory is excluded from Git. Do not push unpublished datasets, passwords, ONCat/SSH credentials, or raw instrument files into this public repository.

## G. Updating after a commit

    cd ~/lab/NeutronToolKit
    git pull --ff-only
    docker compose build
    docker compose run --rm toolkit python -m pytest -q

No ORNL remote connection is needed for these tasks. Athena access can be configured independently when your VCU HPRC account is authorized.

## If Docker Desktop is blocked

Use Micromamba/Miniforge inside Ubuntu as a local environment:
    micromamba create -f environment.yml -y
    micromamba activate neutron-toolkit
    python -m pip install --no-deps -e .
    python -m pytest -q

Do not mix the environment into other lab projects. The Micromamba installation itself must follow the provider's current documentation.


## Blocked Windows WSL installation (0x80370114)

This error commonly indicates a missing Virtual Machine Platform / WSL feature or unavailable virtualization. First check `wsl --status`, `wsl --list --verbose` in PowerShell and the Task Manager CPU virtualization status. Installing Ubuntu again does not enable a missing host feature. On a managed device, ask IT to enable the approved Windows Subsystem for Linux / Virtual Machine Platform features and verify firmware virtualization; this requires administrator-level configuration and possibly a reboot. Do not bypass lab security policy or reinstall/format the laptop.

In the meantime, use the [Open in Colab notebook](../notebooks/NeutronToolKit_Colab_Quickstart.ipynb) from the README; it requires no local WSL or Docker. Only upload files approved for Google cloud processing. For a different no-admin local path later, a per-user Python environment may be permitted, subject to organizational policy and package compatibility.

Official troubleshooting: https://learn.microsoft.com/en-us/windows/wsl/troubleshooting
