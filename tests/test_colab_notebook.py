"""Static Colab launcher contract: GitHub notebook stays valid without executing cloud setup."""
import ast
import json
from pathlib import Path

NOTEBOOK = Path("notebooks/NeutronToolKit_Colab_Quickstart.ipynb")


def test_colab_notebook_is_valid_json_with_python_cells():
    book = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert book["nbformat"] == 4
    assert book["cells"]
    for cell in book["cells"]:
        assert isinstance(cell["source"], list)
        if cell["cell_type"] == "code":
            ast.parse("".join(cell["source"]))


def test_readme_badge_targets_actual_notebook():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "https://colab.research.google.com/assets/colab-badge.svg" in readme
    assert "https://colab.research.google.com/github/kbhalajiyadav/NeutronToolKit/blob/main/" + NOTEBOOK.as_posix() in readme


def test_colab_has_install_and_scientific_examples():
    book = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    text = "\n".join("".join(c["source"]) for c in book["cells"])
    assert "pip" in text and "git" in text and "repo" in text.lower()
    assert "plot_files" in text and "write_sweep" in text
    assert "files.upload()" in text
    assert "No WSL" in text or "without WSL" in text
