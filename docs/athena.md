# VCU Athena profile and permitted job execution

VCU HPRC public documentation describes Athena as Rocky Linux 9, using Slurm and supporting Apptainer on compute nodes. Login host: athena.hprc.vcu.edu. Off-campus access may require the VCU VPN. You need an HPRC account; VCU eID alone does not prove active cluster access.

Repository:
- profiles/vcu-athena.yaml: site details, resource defaults, container runtime, blank SIF/data paths (no secrets)
- scripts/vcu_athena_contrast.sbatch: reviewed CPU job template
- config/ssh_athena.example: optional local SSH host alias

Official references:
- https://research.vcu.edu/resources/cores/hprc/getting-started/
- https://wiki-vcu.atlassian.net/wiki/spaces/unix/pages/45973545/Athena+cluster
- https://wiki-vcu.atlassian.net/wiki/spaces/unix/pages/45976562/Module+Apptainer+Singularity

## Access (when permitted)

1. Follow VCU HPRC account creation instructions and check VPN.
2. In Ubuntu/WSL: ssh YOUR_VCU_EID@athena.hprc.vcu.edu
3. On Athena: module avail; sinfo; command -v apptainer; squeue -u "$USER"
4. Clone the GitHub repository into the approved project directory. Keep data and SIF in institution-approved storage.
5. Provide a validated container image SIF built from the pinned release. Do not assume a public image or use Docker daemon on Athena login nodes.
6. Run a small test batch after the image and account are verified, e.g.:

    export NTK_REPO="$HOME/lab/NeutronToolKit"
    export NTK_IMAGE="/approved/path/neutrontoolkit-validated.sif"
    export NTK_CONFIG="config/deuteration_design_example.json"
    sbatch --export=ALL scripts/vcu_athena_contrast.sbatch
    squeue -u "$USER"

The paths above are PLACEHOLDERS requiring modification. Check local HPRC policy, permissible container creation and allocation. Do not benchmark or fit large models on login nodes.

The Athena profile is currently **descriptive**, not a remote-login or auto-submission feature. The Slurm script contains separately reviewable resource options. The next design stage should generate scheduler templates from profiles after confirming site settings, avoiding duplicate configuration.

## Open OnDemand

VCU also documents an Athena web portal offering JupyterLab and VS Code; this can be easier for students who prefer a browser over remote SSH. It still requires the right account and networking access.

## No ORNL connectivity is required now

The toolkit can work with previously reduced local I(Q) files and synthetic examples. Defer remote ORNL inspection and instrument-specific raw reduction until network and authorized access are available.
