# Optional evidence assistant: constrained open-weight models, not autonomous fitting

**Status:** architecture proposal for AFTER the data/model-validation path works. AI is not required to deliver the 15-day research decision. No model or hosted agent has been deployed or benchmarked.

## What problems an assistant can solve

- Explain why a particular model is eligible, conditional or blocked with citations to upstream documentation and experiment evidence.
- Search permitted SasView/sasmodels model documentation, drtSANS/Mantid reduction references, verified chemical databases and an approved local literature index.
- Turn user intent into typed, reviewable tool requests: inspect a reduced file, retrieve its provenance, evaluate approved model candidates, check compatibility, explain diagnostics, request missing fields.
- Draft an evidence manifest and research report **without** inventing missing calibration, measurement, density, isotope enrichment, material prices or scientific results.

## What it must never be authoritative for

- Numerical SLD, Q calibration, fitting or uncertainty calculations: delegate to validated deterministic libraries.
- Determining structural morphology, phase or molecular dimensions from chemical formula alone.
- Overriding red/amber eligibility rules, applying guessed normalization, creating missing data, selecting a winning model solely by fit score.
- Sending unpublished experimental data, institutional identifiers, instrument access tokens or credentials to arbitrary web endpoints.

## Architecture

1. **Deterministic core:** file parsers, unit/density/SLD calculations, model-library registry, resolution-aware forward models, fit and uncertainty engines and compatibility gates.
2. **Retrieval:** curated allowlisted SasView/sasmodels/drtSANS/Mantid manuals, chemistry references, literature/papers, plus private lab notes **only where the deployment and permissions allow them**. Each retrieved item must have title, version/date, section and URL or local evidence ID.
3. **Assistant model:** small open-weight model with structured tool calling and documented provenance. Propose commands, not scientific facts; all proposed actions must pass backend schema validation, access controls and scientific constraints.
4. **Scientific audit:** source-citation verification; parameter provenance; contradiction/missing-evidence flags; deterministic fit-quality checks; signed-off final interpretation for consequential experiment choices.

Network access should be held by a **restricted retrieval service**, not unrestricted arbitrary web-browsing by the model. Restrict domains, files, quotas and output types; cache/pin docs and record retrieval dates. Treat retrieved text as data, not commands (prompt injection).

## Candidate models to evaluate, not automatically choose

- **IBM Granite 4.0 Micro (3B)**: small Apache-2.0 open-weight family with advertised structured JSON/tool invocation; promising lightweight private UI assistant. Test actual accuracy and tool-call format on lab benchmark.
- **Qwen3 8B**: Apache-2.0 open-weight family with tool-calling support; a second local candidate if more reasoning capacity is needed. Hardware feasibility depends on actual GPU VRAM/quantization, not 64 GB system RAM alone.
- **OpenScholar-8B / its scientific RAG approach**: relevant to literature synthesis and citation-grounded hypothesis retrieval, but not validated to select SAS models or make numerical fits. Check model-specific licenses/weights, infrastructure and current indexing rights before integrating.

Model governance and confidentiality are more important than nominal benchmark rankings. Run without network by default for private data; any search should retrieve public documents without transmitting the sample data.

Primary sources:
https://github.com/ibm-granite/granite-4.0-language-models
https://www.ibm.com/granite/docs/models/granite4-0
https://github.com/QwenLM/Qwen3
https://github.com/AkariAsai/OpenScholar
https://www.nature.com/articles/s41586-025-10072-4

## Should we fine-tune a special neutron model?

**Not initially.** No reliable labeled corpus of "chemical formula -> true SAS morphology" exists for our task, and formula/1D scattering often does not identify a unique structure. Training on synthetic curves from narrow model families risks creating high-confidence but unphysical choices.

After a curated validation set exists, a *small, selective* classifier or reranker could learn which **documentation/evidence cards to inspect next**, not which phase is experimentally true. Its ground truth should be expert-reviewed data/metadata and scientifically justified model eligibility, including explicit negative/inconclusive examples.

## Evaluation before activation

Construct 30–50 diverse, expert-reviewed scenarios with synthetic and approved, redacted real-data metadata:
- Q unit mismatch; I vs counts; dI vs dQ;
- 1D/2D run mismatch; multiple detector configurations; absent calibration;
- chemical formula without density/phase; misleading sphere/rod morphology;
- synthetic Lorentzian vs physically ambiguous scattering; no-model-adequate cases;
- wrong or out-of-date cited source; private data request or hostile retrieved instructions.

Score missing-evidence detection, prohibited equivalence rejection, citation correctness, valid tool schemas, refusal to fabricate numerical parameters and latency. Use a baseline rule-only interface to demonstrate incremental value. Do not deploy a trained model merely because it appears persuasive.

## Decision

For the current research sprint: **No AI deployment or fine-tuning**. Build the deterministic compatibility gate and collect reduction metadata first. After that, run a local assistant benchmark on public synthetic test cases. Adopt only if it demonstrably improves the end-user decision workflow.
