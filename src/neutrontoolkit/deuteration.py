"""Enumerate isotope-label scenarios; report contrast proxies, NOT measured I(q)."""
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
import csv
import hashlib
import json
import math

import numpy as np
import periodictable as pt

# H -> D coherent bound scattering-length difference in femtometers.
DELTA_B_FM = 6.671 - (-3.739)
# (Avogadro number) * (fm -> cm) * (cm^-2 -> 10^-6 Angstrom^-2).
CONVERSION = 6.02214076

def _positive(x, title):
    try:
        x = float(x)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{title}: supply a positive numeric value") from exc
    if not math.isfinite(x) or x <= 0:
        raise ValueError(f"{title}: must be finite and positive")
    return x

def _validate(items):
    if not isinstance(items, list) or not 1 <= len(items) <= 8:
        raise ValueError("Supply 1-8 components")
    parsed, used = [], set()
    for item in items:
        ident = item["id"]
        if not isinstance(ident, str) or not ident.isidentifier() or ident in used:
            raise ValueError("Component IDs must be unique identifiers")
        used.add(ident)
        f = pt.formula(item["formula_H"])
        h_total = float(f.atoms.get(pt.H, 0))
        rho = _positive(item["density_H_g_cm3"], ident + " density")
        volume = float(f.mass)/rho
        sites, h_count_total = [], 0
        for site_name, site in item["sites"].items():
            h_count = int(site["h_count"])
            h_count_total += h_count
            fractions = [float(v) for v in site["fractions"]]
            if h_count <= 0 or not fractions or 0.0 not in fractions:
                raise ValueError("Site must have positive H count and fractions containing 0")
            if len(set(fractions)) != len(fractions) or any(
                not math.isfinite(v) or not 0 <= v <= 1 for v in fractions
            ):
                raise ValueError("Label fractions must be unique and between zero and one")
            price = site.get("incremental_usd_per_mol_fully_labeled")
            if price is not None:
                price = float(price)
                if not math.isfinite(price) or price < 0:
                    raise ValueError("Quote must be nonnegative")
            sites.append((site_name, h_count, sorted(fractions), price))
        if not math.isclose(h_count_total, h_total, abs_tol=1e-8):
            raise ValueError(f"{ident}: formula has {h_total} H but sites sum to {h_count_total}")
        parsed.append({
            "id": ident, "mass_h": float(f.mass), "volume_mol_cm3": volume,
            "sld_h": float(pt.neutron_sld(f, density=rho)[0]), "sites": sites
        })
    return parsed

def _pareto(rows, resource_key):
    ordered = sorted(rows, key=lambda r: (
        r[resource_key], -r["component_variance_proxy"], r["labeling"]
    ))
    frontier, best = [], -1.0
    for row in ordered:
        if row["component_variance_proxy"] > best + 1e-12:
            frontier.append(row)
            best = row["component_variance_proxy"]
    return frontier

def sweep(config):
    comps = _validate(config["components"])
    ref_mass = _positive(config.get("reference_batch_H_g", 1.0), "reference_batch_H_g")
    mixtures = config["compositions"]
    sites = [(i, site_name, n, fractions, quote)
             for i, c in enumerate(comps)
             for site_name, n, fractions, quote in c["sites"]]
    n_scenarios = len(mixtures)*math.prod(len(s[3]) for s in sites)
    if n_scenarios > int(config.get("max_scenarios", 25000)):
        raise ValueError(f"Scenario count {n_scenarios} exceeds configured limit")
    output = []
    for mix in mixtures:
        weight = np.asarray(mix["protonated_mass_fractions"], dtype=float)
        if (len(weight) != len(comps) or np.any(~np.isfinite(weight))
            or np.any(weight < 0) or not np.isclose(weight.sum(), 1.0, atol=1e-8)):
            raise ValueError("Reference protonated mass fractions must be nonnegative and sum to 1")
        mol = ref_mass*weight/np.asarray([c["mass_h"] for c in comps])
        volume = mol*np.asarray([c["volume_mol_cm3"] for c in comps])
        phi = volume/volume.sum()
        for choice in product(*(s[3] for s in sites)):
            nD = np.zeros(len(comps))
            price = 0.0
            missing_quote = False
            label = {}
            for (i, site_name, n, fractions, quote), level in zip(sites, choice):
                nD[i] += n*level
                label[comps[i]["id"] + "." + site_name] = level
                if level > 0 and mol[i] > 0:
                    if quote is None:
                        missing_quote = True
                    else:
                        price += float(mol[i])*level*quote
            sld = np.asarray([
                c["sld_h"] + CONVERSION*DELTA_B_FM*nD[i]/c["volume_mol_cm3"]
                for i, c in enumerate(comps)
            ])
            total = float(np.dot(phi, sld))
            variance = float(np.dot(phi, (sld-total)**2))
            isotope_mass = mol*np.asarray([
                c["mass_h"]+float(nD[i])*(pt.D.mass-pt.H.mass)
                for i,c in enumerate(comps)
            ])
            adjusted_weight = isotope_mass/isotope_mass.sum()
            output.append({
                "composition": mix["name"],
                "labeling": ";".join(f"{key}={value:g}" for key,value in label.items()),
                "component_slds": {c["id"]:float(sld[i]) for i,c in enumerate(comps)},
                "component_volume_fractions": {c["id"]:float(phi[i]) for i,c in enumerate(comps)},
                "labeled_actual_mass_fractions": {c["id"]:float(adjusted_weight[i])
                                                  for i,c in enumerate(comps)},
                "bulk_sld": total, "component_variance_proxy": variance,
                "D_atom_mol_per_reference_batch": float(np.dot(mol, nD)),
                "incremental_label_cost_usd_per_reference_batch":
                    None if missing_quote else price
            })
    summaries = []
    for mix in mixtures:
        subset = [r for r in output if r["composition"] == mix["name"]]
        complete_quotes = all(r["incremental_label_cost_usd_per_reference_batch"] is not None
                              for r in subset)
        resource = ("incremental_label_cost_usd_per_reference_batch" if complete_quotes
                    else "D_atom_mol_per_reference_batch")
        winner = max(subset, key=lambda r: r["component_variance_proxy"])
        summaries.append({
            "composition": mix["name"], "candidate_count": len(subset),
            "contrast_proxy_maximum": winner,
            "pareto_resource": resource, "actual_cost_ranking_available": complete_quotes,
            "pareto_frontier": _pareto(subset, resource)
        })
    return {
        "metric": "conditional_component_segregation_SLD_variance",
        "all_scenarios": output, "summaries": summaries,
        "limitations": [
            "Only a coherent SLD/volume-fraction proxy; not a predicted SANS/USANS intensity or three-nanometer peak.",
            "Protonated-reference mass fractions converted to molecular counts; isotope substitution preserves counts.",
            "Assumes isotope-invariant molar volumes, ideal volume additivity and specified H-state densities.",
            "Fractional site enrichment is an ideal isotope average or labeled/unlabeled isotopologue blending assumption.",
            "Site-specific commercial availability and pricing can be nonlinear or missing.",
            "Missing vendor quotes prevent a real-dollar cost optimum. D-atom moles are NOT a purchase cost.",
            "Incoherent hydrogen background, isotope randomness, label purity and possible phase changes need separate validation."
        ]
    }

def write_sweep(config_path, outdir=None):
    path = Path(config_path).resolve()
    result = sweep(json.loads(path.read_text(encoding="utf-8")))
    dest = Path(outdir) if outdir else Path("outputs/deuteration")/path.stem
    dest.mkdir(parents=True, exist_ok=True)
    report = {k:v for k,v in result.items() if k != "all_scenarios"}
    report["config_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    report["created_utc"] = datetime.now(timezone.utc).isoformat()
    (dest/"summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    columns = ["composition", "labeling", "bulk_sld", "component_variance_proxy",
               "D_atom_mol_per_reference_batch", "incremental_label_cost_usd_per_reference_batch",
               "component_slds", "component_volume_fractions", "labeled_actual_mass_fractions"]
    with (dest/"all_scenarios.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in result["all_scenarios"]:
            writer.writerow({col:json.dumps(row[col]) if isinstance(row[col],dict) else row[col]
                             for col in columns})
    return dest/"summary.json"
