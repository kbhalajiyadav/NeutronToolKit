# Install from scratch on a Windows lab laptop

These steps assume Windows 11 and permission to install software. Do not format the laptop or remove a lab-managed WSL environment. Request IT approval if installations are restricted.

## Step 1: WSL2 and Ubuntu (Windows PowerShell, administrator)

Open the Start menu, search for PowerShell, right-click, Run as administrator.

    wsl --status
    wsl --list --verbose

If Ubuntu is missing:

    wsl --install -d Ubuntu

Restart Windows if prompted. Launch Ubuntu from Start, create a Linux username and password. If Ubuntu already exists, do not reinstall it. You can use wsl --update from an elevated PowerShell if required.

## Step 2: Docker Desktop (Windows)

Install Docker Desktop from https://docs.docker.com/desktop/setup/install/windows-install/.
Choose the Linux-containers / WSL2 backend. Open Docker Desktop > Settings > Resources > WSL Integration and enable your Ubuntu distribution. Launch Docker Desktop.

Docker Desktop licensing and enterprise/educational IT policy should be checked for your institution.

## Step 3: VS Code (Windows)

Install https://code.visualstudio.com/ and its WSL and Dev Containers extensions. Optional Jupyter and Python extensions are included in the project's dev container.

## Step 4: Git and source code (Ubuntu, not PowerShell)

Open Ubuntu. Run these commands one by one:

    sudo apt update
    sudo apt install -y git
    mkdir -p ~/lab
    cd ~/lab
    git clone https://github.com/kbhalajiyadav/NeutronToolKit.git
    cd NeutronToolKit
    pwd

Expected location begins with /home/YOUR_LINUX_USER/lab. Do not work from /mnt/c/Users/... for large datasets and container-heavy I/O.

Check:

    git --version
    docker version
    docker compose version

If Docker commands fail, check Docker Desktop is running and Ubuntu integration is enabled.

## Step 5: Build the scientific environment

In Ubuntu, from the NeutronToolKit directory:

    docker compose build

This installs Python, sasmodels, sasdata, bumps, periodictable, Textual and JupyterLab inside a container. This is the long-term shareable runtime. Do not mix this with the PatternReveal environment.

## Step 6: Verify

    docker compose run --rm toolkit python -m neutrontoolkit doctor
    docker compose run --rm toolkit python -m pytest -q
    docker compose run --rm toolkit python -m neutrontoolkit qc data/examples/synthetic_iq.dat

If tests fail, save the full command and error output, and inspect the GitHub Actions checks before lab use.

## Step 7: Browse and plot

    docker compose run --rm toolkit python -m neutrontoolkit browse data/examples

Use Space to select. P generates an overlay in outputs/plots. In the Ubuntu project folder run:

    code .

Open the newly generated PNG or SVG from the VS Code file explorer. For your real data, put reduced ASCII files into data/reduced (not data/examples).

## Step 8: Optional Jupyter

    docker compose up lab

Read the terminal log for the tokenized http://127.0.0.1:8888 address, open it in Windows browser, and use Ctrl+C in the Ubuntu terminal to stop the server. Never publicly expose the Jupyter port or disable the token.

## Step 9: Update later

    cd ~/lab/NeutronToolKit
    git pull --ff-only
    docker compose build

Your private data in data/reduced and plots in outputs remain local. Back up data using approved lab storage.

## Alternative without Docker

On macOS or Linux, install Miniforge/Micromamba, then from the repository:

    micromamba create -f environment.yml -y
    micromamba activate neutron-toolkit
    python -m pip install --no-deps -e .
    python -m pytest -q
    python -m neutrontoolkit browse data/examples

Conda package availability varies by OS/architecture. The Docker workflow provides the common Linux environment; Mac with Apple Silicon runs an ARM-compatible image when available, which still needs testing.

## Troubleshooting

- Docker command not found in Ubuntu: enable Docker Desktop WSL Integration.
- Docker permission/daemon error: start Docker Desktop; do not install a second unrelated daemon into Ubuntu.
- No files in terminal: point browser at data/examples first; place real reduced data under data/reduced.
- No GUI figure opens when pressing P: expected for headless Docker; files are saved under outputs/plots.
- Raw NeXus fails to load: intentional in v0.1; first reduce via ORNL drtsans/Mantid or an approved instrument workflow.
- Unrecognized data columns: use header lines followed by ascending numerical Q, I, optional dI, optional dQ; verify column order before analysis.
