# Colab, Binder, Streamlit: browser-based choices

## Recommended order

For a fresh managed Windows lab laptop without administrator rights:
1. Use the Google Colab quickstart badge at the top of README today. Run its first setup cell until it prints "Import success".
2. Use the bundled synthetic curve, model preview, and H/D contrast design. Avoid uploading unpublished research data without VCU/ORNL authorization.
3. Use the Streamlit browser adapter for a more beginner-friendly integrated interface. This repository has the app source, but it has NOT yet been publicly deployed to Streamlit Community Cloud.
4. Use the local Conda/WSL or VCU Athena backends for sustained research analysis once approved.

## Streamlit: best eventual beginner interface

Streamlit app entrypoint: apps/streamlit_app.py.

It currently offers:
- browse/filter and select reduced 1D sample files, from synthetic examples or authorized uploads
- I(Q), Guinier, Kratky, and Porod plots, QC and downloads
- illustrative isotope-labeling fraction scenario sweep and CSV export
- model eligibility guide from the same validated scientific package

The app is a view/wrapper over src/neutrontoolkit; there are NO duplicate scattering formulas or fitting algorithms in the UI.

To run in a permitted local scientific environment:

    python -m pip install -r requirements.txt
    streamlit run apps/streamlit_app.py

No-admin hosted deployment is possible through https://share.streamlit.io with a GitHub account. To deploy manually, authorize the GitHub connection and select:
- Repository: kbhalajiyadav/NeutronToolKit
- Branch: main
- Main file: apps/streamlit_app.py

The root requirements.txt installs the package and Streamlit. Deployment success, hosted URL, and privacy are NOT guaranteed until verified. Never publicize private data in a demo cloud app.

## Colab: fastest option today

Notebook:
https://colab.research.google.com/github/kbhalajiyadav/NeutronToolKit/blob/main/notebooks/NeutronToolKit_Colab_Quickstart.ipynb

It requires no WSL or Docker. Notebook cells are explanatory and easily modified for research. The first setup cell clones and installs from GitHub. If the doctor cell raises ModuleNotFoundError, the install cell has either not run or failed, or the Colab runtime has been reset. Rerun it and check for the "Import success" message.

The notebook has a smaller filter/multi-selection widget panel in Section 7. The full Streamlit app is not automatically available inside Colab; it is a separate browser deployment.

## Binder: optional demonstrator

https://mybinder.org can build a repo with an environment.yml and serve JupyterLab. It is valuable for reproducible tutorials and anonymous open-science demonstrations, but the shared public service has CPU/memory/session limits and idle culling. It is not the preferred default for large fitting jobs or persistent laboratory data. We have NOT deployed or validated a Binder link for this repository; the presence of an environment.yml is not proof that a custom Dockerfile will launch under Binder's requirements.

## Maintainability rule

Only core package modules implement scientific calculations. Colab, Streamlit, the Textual terminal browser and eventual HPC adapters import these same modules.

Sources:
https://research.google.com/colaboratory/faq.html
https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html
https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/quickstart
