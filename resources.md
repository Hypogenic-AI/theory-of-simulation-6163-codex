# Resources Catalog

## Summary

This document catalogs the resources gathered for the project on simulation theory for LLMs, including papers, datasets, and code repositories relevant to human-behavior simulation, demographic alignment, and agent-based evaluation.

## Papers

Total papers downloaded: 10

| Title | Year | File | Key Info |
|-------|------|------|----------|
| Generative Agents: Interactive Simulacra of Human Behavior | 2023 | `papers/generative_agents_interactive_simulacra_of_human_behavior.pdf` | Foundational memory-planning-reflection simulator |
| Social Simulacra | 2022 | `papers/social_simulacra_creating_populated_prototypes.pdf` | Early population simulation for social systems |
| Using LLMs to Simulate Multiple Humans | 2023 | `papers/using_llms_to_simulate_multiple_humans.pdf` | Turing Experiments for simulation fidelity |
| Whose Opinions Do Language Models Reflect? | 2023 | `papers/whose_opinions_do_language_models_reflect.pdf` | OpinionQA benchmark and alignment metrics |
| S^3 | 2023 | `papers/s3_social_network_simulation_system.pdf` | Social-network simulation with LLM agents |
| LLMs Simulate Big Five Personality Traits | 2024 | `papers/llms_simulate_big_five_personality_traits.pdf` | Personality-conditioning evidence |
| LLMs as linguistic simulators and cognitive models | 2024 | `papers/llms_as_linguistic_simulators_and_cognitive_models.pdf` | Best conceptual framing paper |
| Can LLM Agents Simulate Human Trust Behavior? | 2024 | `papers/can_llm_agents_simulate_human_trust_behaviors.pdf` | Controlled trust benchmark with code |
| LLMs Assume People are More Rational than We Really Are | 2025 | `papers/llms_assume_people_are_more_rational.pdf` | Key negative result on rationality bias |
| OmniBehavior | 2026 | `papers/omnibehavior_benchmarking_llms_on_real_world_human_behavior.pdf` | Long-horizon real-world benchmark |

See `papers/README.md` for details.

## Datasets

Total datasets downloaded: 3

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| OpinionQA | Hugging Face | 294 val / 882 test | demographic opinion alignment | `datasets/opinionqa/` | Mirrors paper benchmark structure |
| Synthetic-Persona-Chat | Hugging Face | 8938 train / 1000 val / 968 test | persona-conditioned dialogue | `datasets/synthetic_persona_chat/` | Auxiliary latent-factor conditioning data |
| Social IQa | Hugging Face mirror | 33410 train / 1954 val | social commonsense choice prediction | `datasets/social_i_qa/` | Mirror used because original script-based Hub entry failed |

See `datasets/README.md` for download instructions and samples.

## Code Repositories

Total repositories cloned: 5

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| generative_agents | github.com/joonspk-research/generative_agents | Smallville agent simulator | `code/generative_agents/` | Original implementation, large clone |
| agent_trust | github.com/camel-ai/agent-trust | Trust Game alignment experiments | `code/agent_trust/` | Best controlled behavioral benchmark repo here |
| opinions_qa | github.com/tatsu-lab/opinions_qa | OpinionQA analysis | `code/opinions_qa/` | Useful metrics notebooks |
| turing_experiments | github.com/microsoft/turing-experiments | Simulated human-subject studies | `code/turing_experiments/` | Large repo, full data may require Git LFS |
| concordia | github.com/google-deepmind/concordia | General social simulation library | `code/concordia/` | Best reusable framework |

See `code/README.md` for details.

## Resource Gathering Notes

### Search Strategy

I first attempted the local `paper-finder` workflow in diligent mode, then fell back to manual discovery through arXiv, Hugging Face dataset pages, and GitHub because the local search round did not return in a useful time window. I prioritized papers with direct behavioral claims, benchmark papers, and papers with released code or datasets.

### Selection Criteria

- Direct relevance to human-behavior simulation
- Strong evaluation methodology
- Publicly accessible paper PDFs
- Practical value for downstream experiments
- Coverage across conceptual, benchmark, and systems layers

### Challenges Encountered

- The local paper-finder workflow stalled, so manual search was necessary.
- One PDF download was truncated and had to be re-fetched directly from arXiv.
- The original `allenai/social_i_qa` Hub entry relied on an unsupported dataset script, so a mirror was used instead.
- Some repos require API keys, Git LFS, or heavyweight external dependencies, so only README-level validation was feasible in this pass.

### Gaps and Workarounds

- OmniBehavior appears to be the best recent benchmark, but full public data release may be pending audit. Workaround: use OpinionQA and controlled task benchmarks now, then integrate OmniBehavior once data/code are public.
- Public datasets for true long-horizon, individual-level human traces remain scarce. Workaround: combine demographic alignment data with scenario-level choice tasks and persona corpora.

## Recommendations for Experiment Design

1. **Primary dataset(s)**: `OpinionQA` for group-level alignment and `social_i_qa` for local decision prediction. Use `Synthetic-Persona-Chat` only to construct or regularize persona prompts.
2. **Baseline methods**: unconditioned base/instruction LLM, demographic-conditioned prompting, persona-conditioned prompting, expected-value baseline for risky decisions, and memory-enabled agents via Concordia or Generative Agents.
3. **Evaluation metrics**: distribution alignment, discrete-choice accuracy, calibration, subgroup coverage, entropy/diversity preservation, and long-tail behavior recall.
4. **Code to adapt/reuse**: `opinions_qa` for metrics, `agent_trust` for behavioral-game scaffolding, `turing_experiments` for replication design patterns, and `concordia` for new multi-agent simulations.
