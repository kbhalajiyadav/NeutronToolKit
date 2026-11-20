"""Static check that the Streamlit adapter remains importable Python source."""
import ast
from pathlib import Path

def test_streamlit_source_syntax():
    code = Path("apps/streamlit_app.py").read_text(encoding="utf-8")
    ast.parse(code)
    assert "from neutrontoolkit.plots import plot_files" in code
    assert "from neutrontoolkit.deuteration import sweep" in code
    assert "st.file_uploader" in code
    assert "st.download_button" in code

def test_requirements_have_editable_project():
    requirements = Path("requirements.txt").read_text()
    assert "-e ." in requirements
    assert "streamlit" in requirements
