"""Batch commands share the same analysis functions as the interactive terminal."""
import argparse
import importlib.metadata
import json
import platform
import sys

def make_parser():
    p = argparse.ArgumentParser(prog="ntk", description="NeutronToolKit scientific data tools")
    sub = p.add_subparsers(dest="command", required=True)
    x = sub.add_parser("browse", help="Interactive reduced-data file browser")
    x.add_argument("folder", nargs="?", default="data/reduced")
    x = sub.add_parser("qc", help="Validate reduced 1D files")
    x.add_argument("files", nargs="+")
    x = sub.add_parser("plot", help="Save I(Q), Kratky, Porod or Guinier plots")
    x.add_argument("files", nargs="+")
    x.add_argument("--kind", choices=("iq", "kratky", "porod", "guinier"), default="iq")
    x.add_argument("--outdir", default="outputs/plots")
    x = sub.add_parser("sld", help="Neutron coherent SLD, with explicit density")
    x.add_argument("formula")
    x.add_argument("--density", type=float, required=True)
    x = sub.add_parser("mix-sld", help="Mixture neutron coherent SLD")
    x.add_argument("json_config")
    x = sub.add_parser("simulate", help="Sasmodels theory preview, not a fit")
    x.add_argument("json_config")
    x.add_argument("--data")
    x.add_argument("--outdir", default="outputs/models")
    x = sub.add_parser("guide", help="Physics-gated model hypothesis suggestions")
    x.add_argument("json_config")
    x = sub.add_parser("compare", help="Fit competing sasmodels hypotheses with bounded least squares")
    x.add_argument("json_config")
    x.add_argument("--outdir")
    x = sub.add_parser("plan-runs", help="Dry-run instrument metadata matching; no reduction")
    x.add_argument("csv_manifest")
    x.add_argument("--out", default="outputs/reduction/matching_plan.json")
    x = sub.add_parser("contrast-sweep", help="Enumerate isotope label fractions and reference compositions")
    x.add_argument("json_config")
    x.add_argument("--outdir")
    sub.add_parser("doctor", help="Check scientific dependency installation")
    return p

def doctor():
    names = ("numpy", "matplotlib", "scipy", "periodictable", "sasmodels",
             "sasdata", "bumps", "textual")
    result = {"python": sys.version.split()[0], "platform": platform.platform(), "packages": {}}
    for name in names:
        try:
            result["packages"][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            result["packages"][name] = "NOT INSTALLED"
    return result

def main(argv=None):
    a = make_parser().parse_args(argv)
    try:
        if a.command == "doctor":
            print(json.dumps(doctor(), indent=2))
        elif a.command == "browse":
            from .tui import DataBrowser
            DataBrowser(a.folder).run()
        elif a.command == "qc":
            from .files import load, quality
            for file in a.files:
                print(json.dumps(quality(load(file)), indent=2))
        elif a.command == "plot":
            from .plots import plot_files
            print(plot_files(a.files, a.kind, a.outdir))
        elif a.command == "sld":
            from .contrast import sld
            print(json.dumps({"formula": a.formula, "density_g_cm3": a.density,
                              "coherent_sld_1e-6_A-2": sld(a.formula, a.density)}, indent=2))
        elif a.command == "mix-sld":
            from .contrast import from_json
            print(json.dumps(from_json(a.json_config), indent=2))
        elif a.command == "guide":
            from .model_rules import from_file
            print(json.dumps(from_file(a.json_config), indent=2))
        elif a.command == "compare":
            from .fitting import compare
            print(compare(a.json_config, a.outdir))
        elif a.command == "plan-runs":
            from .run_manifest import write_plan
            print(write_plan(a.csv_manifest, a.out))
        elif a.command == "contrast-sweep":
            from .deuteration import write_sweep
            print(write_sweep(a.json_config, a.outdir))
        elif a.command == "simulate":
            from .models import preview
            print(preview(a.json_config, a.data, a.outdir))
    except (ValueError, OSError, ImportError, KeyError) as exc:
        print(f"NeutronToolKit error: {exc}", file=sys.stderr)
        return 2
    return 0
