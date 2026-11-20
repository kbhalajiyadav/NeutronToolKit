# Product brief: solve the neutron end user's decision problem

## Product promise

NeutronToolKit helps a novice or experienced scattering user go from reduced experimental data to an evidence-qualified conclusion (or an explicit *inconclusive* outcome), with reproducible analysis, accessible explanations and suggested next measurements. This is NOT an additional library of form factors, a replacement for SasView, or a facility-certified reduction engine.

## Users and jobs to be done

| User | Actual problem | Job outcome |
|---|---|---|
| First-time SANS/USANS student | "What are these files, what is missing, and can I plot or fit them?" | Guided import and meaningful data-quality blockers |
| Soft-matter researcher | "Which model is physically appropriate, and which parameters can my data resolve?" | Candidate hypotheses with evidence and quantified model failures |
| Beamline scientist | "Can users reproduce reductions, provide metadata, and avoid invalid claims?" | Instrument-aware provenance, facility backend interoperability and audit bundles |
| Lab group / PI | "Can someone else rerun this analysis and explain the science?" | Reproducible versioned report and limitations |
| Multi-contrast experimentalist | "What experiment would distinguish my competing hypotheses?" | Uncertainty-aware next-measurement recommendations, after validated forward models |

## End-to-end product journey

1. **Open data.** Accept reduced 1D first; recognize unsupported raw/2D formats honestly. Import unit metadata and related detector configurations.
2. **Understand data quality.** Check numerical integrity, uncertainty, signal/background, Q range, resolution provenance and experimental metadata. Say why a gate fails.
3. **Describe observations without overclaiming.** Identify candidate knees, broad peaks and scaling intervals, their sensitivity to fit windows and Q resolution.
4. **Describe the sample.** Accept formula/structure, composition, density, temperature, phase and any independent evidence. Every parameter has a measured/calculated/literature/estimated/hypothetical source.
5. **Consider models.** Use native sasmodels metadata and curated physical eligibility cards. Show not only proposed models but those ruled out and why.
6. **Fit and challenge.** Use sasmodels/Bumps and documented likelihood/resolution; compare candidates on the same data with reproducible diagnostics.
7. **Explain the decision.** Separate empirical feature from physical interpretation, state unidentifiable parameters, and provide an **INCONCLUSIVE** or **NO MODEL ADEQUATE** outcome.
8. **Recommend useful next evidence.** Suggest an experiment or contrast that could distinguish remaining hypotheses; do not automatically promote more complex fitting.
9. **Share reproducibly.** Save figures, manifests, source hashes, package versions, parameter provenance, uncertainties and caveats. Raw/private lab data remain in approved storage.

## First shipped end-user capability: triage

Command (local, Conda, Docker, Colab, or approved institutional environment):

    python -m neutrontoolkit triage data/examples/synthetic_iq.dat
    python -m neutrontoolkit triage data/reduced/approved_sample.dat --context config/triage_context_example.json

Outputs: `outputs/triage/triage.json` and `outputs/triage/NEXT_STEPS.md`. Triage reuses the existing strict reduced-data loader, checks uncertainties, displays measured Q coverage and explains missing instrument metadata. It intentionally makes NO automatic structural identification, guessed dQ resolution or hidden facility calls.

The example context is synthetic and contains nulls for unknown experimental conditions. Missing metadata are a documented research task, not silently filled by a guessed default.

## MVP acceptance criteria

The first practical product release must pass:
- A beginner can identify supported files, QC results and exact missing metadata without writing Python.
- Existing synthetic data and one authorized private reference dataset generate comparable reports on Colab and local Conda with declared environment versions.
- Every fit reports instrument resolution source, likelihood assumptions, model provenance, parameter constraints and residual diagnostics, or explicitly blocks quantitative interpretation.
- Any model recommendation distinguishes empirical description from physically eligible hypotheses.
- Failed or ambiguous hypotheses produce an explicit *inconclusive* conclusion rather than a misleading ranked winner.
- Re-running the same version/configuration recreates results within numerical tolerance; source/data hashes are recorded.
- Sensitive datasets are neither published to public GitHub nor uploaded to third-party clouds without approval.

## Not in first product release

Do not divert development to automatic raw ORNL event reduction, every SAS model, general AI structure discovery, molecular dynamics, GPU acceleration, public-cloud storage of experiments, supplier cost optimization, or a new graphical UI framework. Connect facility-specific and HPC backends only after the data/fit validation path is reliable.

## Product metrics (test against real people)

- Fraction of novice users who complete validated import/QC without assistance.
- Correctness of warnings on deliberately corrupted/mislabeled datasets.
- Rate of unsupported conclusions blocked in benchmark cases.
- Reproducibility across specified environments and software versions.
- Time from reduced data to an auditable report, with no hidden assumptions.
- Number of independent scientifically valid hypotheses distinguished, not just fit success rate.

**Scope-control rule:** every proposed feature must remove a documented user obstacle and reuse a trusted upstream scientific engine where one exists.
