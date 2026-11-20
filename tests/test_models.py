from neutrontoolkit.models import preview

def test_fixed_parameter_preview(tmp_path):
    target = preview("config/example_sphere.json", outdir=tmp_path)
    assert target.is_file()
    assert (tmp_path / "model_overlay.json").is_file()
