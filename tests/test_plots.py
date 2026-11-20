from pathlib import Path
from neutrontoolkit.files import load
from neutrontoolkit.plots import transform, plot_files

def test_plot_generation(tmp_path):
    figure = plot_files(["data/examples/synthetic_iq.dat"], outdir=tmp_path)
    assert figure.is_file()
    assert figure.with_suffix(".svg").is_file()
    assert figure.with_suffix(".json").is_file()

def test_plot_transforms():
    curve = load("data/examples/synthetic_iq.dat")
    for kind in ("iq", "kratky", "porod", "guinier"):
        x, y, dy, xl, yl = transform(curve, kind)
        assert len(x) == len(y) == 11
