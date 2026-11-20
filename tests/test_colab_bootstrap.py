"""Regression checks for the no-admin Colab notebook source."""
import ast
import json
from pathlib import Path

NOTEBOOK = Path("notebooks/NeutronToolKit_Colab_Quickstart.ipynb")

def test_notebook_import_bootstrap_and_syntax():
    book = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert book["nbformat"] == 4
    code_cells = [cell for cell in book["cells"] if cell["cell_type"] == "code"]
    for cell in code_cells:
        ast.parse("".join(cell["source"]))
    setup = next(cell for cell in code_cells if cell.get("id") == "install")
    source = "".join(setup["source"])
    assert "sys.executable" in source
    assert "Import success" in source
    assert "sys.path.insert" in source

def test_readme_colab_badge_link():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "https://colab.research.google.com/assets/colab-badge.svg" in readme
    assert "NeutronToolKit_Colab_Quickstart.ipynb" in readme
