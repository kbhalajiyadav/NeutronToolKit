# Google Colab: no WSL, no Docker, no administrator rights

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kbhalajiyadav/NeutronToolKit/blob/main/notebooks/NeutronToolKit_Colab_Quickstart.ipynb)

Colab opens a notebook directly from the public GitHub repository on a temporary Google-managed Python virtual machine. You need a browser, internet access, and a Google account. You do **not** need WSL, a local Python installation or Docker Desktop.

## Starting

1. Click the Open in Colab badge above (or in README).
2. Choose **Connect**; use the default CPU runtime, not a paid GPU.
3. Run **Section 1: Install the current toolkit**. The cell clones GitHub and installs Python dependencies for this session. Colab software versions can change.
4. Run **Section 2: Check the scientific environment**.
5. Run **Section 3** to view a synthetic I(Q) example; Section 4 to preview a SasView engine model, and Section 5 for the isotope-design scenario sweep.
6. Only if authorized, use Sections 6–7 to upload reduced 1D scattering ASCII files and choose plots with filter/select widgets.
7. Download results using Section 8 before your session is deleted.

## How this compares to the terminal

Colab notebooks do not run Docker containers and do not expose the terminal Textual interface. Section 7 offers an analogous file-selection widget. It supports filtering filenames, multi-select, changing plot type, clearing selections and displaying graphs.

## Supported now

Reduced 1D file validation, plotting, SasView-engine model preview, model-guidance rules, and isotope scenario screening. The included dataset and example model are teaching demos. This does **not** automatically reduce raw ORNL data or establish the best physical model of a cholesteric mixture. The H/D module currently reports a conditional SLD variance proxy and cannot predict experimental peak heights or vendor costs without extra inputs.

## Privacy and persistence

Colab runtimes are cloud-hosted and ephemeral. Uploaded data and generated plots may disappear on disconnection. Store lab data in institution-approved services, never public Git, and only upload ORNL/VCU experimental data if cloud transfer is authorized. The public synthetic examples are safe for demonstration. Download your generated output ZIP when finished.

## Reproducibility

The bootstrap prints the Git commit SHA and Python version. Colab follows the moving default GitHub branch and its package ecosystem, so results are **not** reproducible bit-for-bit by default. For reference-quality analysis, freeze the repository commit, record scientific package versions, and validate results against the Docker/Conda CI and instrument-specific data.

## Limitations

- Colab has usage limits and temporary runtime lifetime; no guarantee of continuous high-performance computing.
- The notebook does not connect to authorized ORNL or VCU Athena accounts.
- Hosting confidential files in Colab can violate lab policies; use approved computing for restricted research.
- Widget availability can change; core notebook cells still support direct Python analysis if widgets do not render.

Sources:
- https://research.google.com/colaboratory/faq.html
- https://colab.research.google.com/notebooks/snippets/advanced_outputs.ipynb
