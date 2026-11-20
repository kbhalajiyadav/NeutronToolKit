# Deuteration scenario screening: physics, cost, limitations

## Objective

Find feasible site-selective isotopic labeling combinations and formulation ratios that improve experimentally relevant contrast subject to **real purchase quotes and structural evidence**.

Use:
    python -m neutrontoolkit contrast-sweep config/deuteration_design_example.json

Or with Docker:
    docker compose run --rm toolkit python -m neutrontoolkit contrast-sweep config/deuteration_design_example.json

Results:
- outputs/deuteration/deuteration_design_example/all_scenarios.csv
- outputs/deuteration/deuteration_design_example/summary.json

The example explores three cholesterol-derived components:
- COC C46H80O3: 45 cholesteryl hydrogens and 35 oleyl-tail hydrogens.
- CP C36H62O2: 45 cholesteryl hydrogens and 17 pelargonate-tail hydrogens.
- CC C27H45Cl: 45 cholesteryl hydrogens, no separate ester/carbonate tail.
Fractions are declared as site-level nominal D fractions; not promised supplier products. Composition ratios include 20:40:40, 80:10:10, 52:24:24 and 38:31:31 on *protonated-component mass basis*. Verify every real sample formulation independently.

## Mathematical definition

Given protonated mass fractions w_i and molar masses M_i, the fixed reference moles are n_i = w_i * batch_mass / M_i. Under the explicit invariant-molar-volume approximation V_i = M_i/rho_H,i, the volume fractions are phi_i = n_i*V_i / sum_j(n_j*V_j).

With h_ij replaceable hydrogens at site j and nominal labeling fraction x_ij, the expected number of D per molecule is N_D,i = sum_j(h_ij*x_ij).
Coherent SLD in units of 10^-6 A^-2:
rho_i = rho_i,H + (6.02214076)*(b_D-b_H in fm)*N_D,i / (V_i in cm3/mol).
Uses PeriodicTable for rho_i,H and molecular weights; b_D-b_H approx 10.410 fm.

If isotopic substitution changes molecular mass but *not moles*, the actual new mass fractions differ from the stated H-reference fractions; the report gives both.

For putative *component segregation* the optional descriptor is:
V_SLD = sum_i phi_i * (rho_i - sum_j(phi_j*rho_j))^2.
This is not the predicted intensity of a homogeneous mixed cholesteric state, not a validated 3 nm peak amplification, and not a model of steroid-core/alkyl-tail layering. It only ranks a conditional component-SLD variance.

For a measured three-nanometer SANS feature, a separate SLD profile/correlation model with fragment volumes and molecular packing is needed, using sasmodels and instrumental resolution. Incoherent scattering (especially H), isotope-enrichment variation, sample thickness, transmission, and changes in phase/pitch must be included before experimental recommendations.

## Lowest investment requires quotes

Input incremental_usd_per_mol_fully_labeled for each permitted site if you have a grounded quote or justified cost model. The current implementation assumes **linearized incremental site pricing** for partially labeled fractions. This is an economic approximation, not a vendor promise. If any needed quote is absent, the report refuses to assign a dollar cost optimum; instead it supplies a frontier in *moles of deuterium atoms used*, explicitly labeled a non-financial proxy.

To estimate actual cost, add vendor availability, isotopic purity, minimum order quantity, synthesis/setup fees, yield and lead time. Do not equate fewer isotope atoms with cheaper synthesis.

For sampling dozens of sites with many percentage increments, use pruning or adaptive optimization to control the full combinatorial grid before HPC. The small example is appropriate for a laptop and does not need HPC.

Sources:
- https://periodictable.readthedocs.io/en/latest/api/nsf.html
- https://www.ncnr.nist.gov/resources/sldcalc.html
- https://www.sasview.org/docs/dev/sasmodels-api/direct_model.html
