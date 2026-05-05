# Literature Review: A theory of simulation

> Created: 2026-05-05
> Last Updated: 2026-05-05

## Review Scope

### Research Question

What would a theory of simulation look like for LLMs, and under what conditions can LLMs that capture latent factors behind human behavior simulate not just average human responses but a superset of plausible human outcomes?

### Inclusion Criteria

Papers are included if they:
- Study LLMs as simulators, proxies, or evaluators of human behavior.
- Provide concrete experiments, datasets, or code relevant to behavioral alignment.
- Help operationalize latent factors such as trust, rationality, opinions, or personas.

### Exclusion Criteria

Papers are excluded if they:
- Focus only on generic autonomous agents without human-behavior grounding.
- Study dialogue quality without behavioral or cognitive claims.
- Are primarily about robotics or embodied control without relevance to human simulation.

### Time Frame

2022 to 2026, with emphasis on 2023 to 2025 and one very recent benchmark from April 9, 2026.

### Search Sources

- arXiv
- Hugging Face papers / datasets
- GitHub
- Papers with Code / project pages when available

## Search Log

| Date | Query | Source | Results | Relevant | Notes |
|------|-------|--------|---------|----------|-------|
| 2026-05-05 | `theory of simulation large language models human behavior latent factors` | local paper-finder + manual | paper-finder stalled | 0 direct | fell back to manual search |
| 2026-05-05 | `large language models human behavior simulation` | arXiv / web | multiple | high | identified simulation and benchmark papers |
| 2026-05-05 | `language models opinions reflect` | arXiv / GitHub | multiple | high | identified OpinionQA |
| 2026-05-05 | `human trust behavior llm agents` | arXiv / GitHub | multiple | high | identified NeurIPS 2024 trust paper and code |
| 2026-05-05 | `real-world human behavior simulation benchmark llm` | arXiv / web | multiple | medium-high | identified OmniBehavior, dated 2026-04-09 |

## Screening Summary

Records identified: 10 core papers downloaded
After deduplication: 10
Title screened: 10
Abstract screened: 10
Full-text skimmed/chunked: 5 priority papers
Included in review: 10

## Key Papers

### Generative Agents: Interactive Simulacra of Human Behavior (2023)
- **Authors**: Park et al.
- **Source**: UIST / arXiv 2304.03442
- **Key Contribution**: Canonical architecture for believable agent behavior using observation, planning, and reflection loops.
- **Methodology**: 25 agents in a Smallville sandbox; memory stream plus retrieval weighted by recency, importance, and relevance; reflection synthesizes higher-level beliefs.
- **Datasets Used**: No external human dataset; simulated town environment and human evaluator study.
- **Results**: Agents show believable emergent coordination, such as party planning and invitation propagation; ablations show observation, planning, and reflection each matter.
- **Code Available**: Yes, `joonspk-research/generative_agents`
- **Relevance to Our Research**: Useful for building process-level simulation architectures, but weak on formal fidelity to real human distributions.

### Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies (2023)
- **Authors**: Aher, Arriaga, Kalai
- **Source**: ICML / arXiv 2208.10264
- **Key Contribution**: Introduces Turing Experiments as a concrete test of simulation fidelity.
- **Methodology**: Zero-shot prompts used to simulate representative participants in Ultimatum Game, Garden Path, Milgram, and Wisdom of Crowds studies.
- **Datasets Used**: Human-subject study stimuli and result files for the four experiments.
- **Results**: Three classic findings replicate; Wisdom of Crowds reveals a hyper-accuracy distortion.
- **Code Available**: Yes, `microsoft/turing-experiments`
- **Relevance to Our Research**: Strong evaluation framing for whether an LLM simulates a distribution of humans rather than one idealized person.

### Whose Opinions Do Language Models Reflect? (2023)
- **Authors**: Santurkar et al.
- **Source**: arXiv 2303.17548
- **Key Contribution**: OpinionQA benchmark and representativeness metrics over 60 US demographic groups.
- **Methodology**: Public opinion survey questions from Pew ATP converted into model prompts; compares LM opinion distributions with demographic distributions.
- **Datasets Used**: OpinionQA, 1498 multiple-choice questions.
- **Results**: Substantial group-level misalignment persists even under demographic steering; some groups are systematically underrepresented.
- **Code Available**: Yes, `tatsu-lab/opinions_qa`
- **Relevance to Our Research**: Essential for testing whether a simulator captures latent demographic structure instead of only average opinions.

### Large language models as linguistic simulators and cognitive models in human research (2024)
- **Author**: Zhicheng Lin
- **Source**: arXiv 2402.04470
- **Key Contribution**: Clarifies that LLMs should be treated as pragmatic simulators and cognitive models, not replacements for human participants.
- **Methodology**: Conceptual analysis organized around six fallacies and four validity concerns.
- **Datasets Used**: None; methodology paper.
- **Results**: Provides safeguards around internal, external, construct, and statistical validity.
- **Code Available**: No
- **Relevance to Our Research**: Best conceptual scaffold for a theory of simulation. It supports a validated-simulator view rather than a substitution view.

### Can Large Language Model Agents Simulate Human Trust Behavior? (2024)
- **Authors**: Xie et al.
- **Source**: NeurIPS 2024 / arXiv 2402.04559
- **Key Contribution**: Strong evidence that GPT-4-class agents can align with human trust behavior in controlled economic games.
- **Methodology**: Trust Games with BDI-style personas; probes reciprocity anticipation, risk perception, prosocial preference, demographic manipulations, and repeated interactions.
- **Datasets Used**: Trust Game setups and comparisons against existing human trust findings.
- **Results**: GPT-4 shows the closest behavioral alignment; smaller models align worse; trust is manipulable and context-sensitive.
- **Code Available**: Yes, `camel-ai/agent-trust`
- **Relevance to Our Research**: Shows one path toward latent-factor simulation: capture a constrained behavioral primitive and test alignment carefully.

### LLMs Simulate Big Five Personality Traits: Further Evidence (2024)
- **Authors**: Sorokovikova et al.
- **Source**: arXiv 2402.01765
- **Key Contribution**: Tests stability and expressibility of personality traits in LLM role-play.
- **Methodology**: Big Five prompting and trait analysis across several LLMs.
- **Datasets Used**: Personality assessment framing rather than a benchmark corpus.
- **Results**: LLMs can express trait-like differences, but stability and realism remain open.
- **Code Available**: Not identified in this pass.
- **Relevance to Our Research**: Supports the idea that latent factors can be parameterized, but not yet that they are causally faithful.

### Large Language Models Assume People are More Rational than We Really Are (2025)
- **Authors**: Liu et al.
- **Source**: ICLR 2025 / arXiv 2406.17055
- **Key Contribution**: Identifies a systematic distortion: LLMs overestimate rationality in human decisions.
- **Methodology**: Forward-modeling risky choices and inverse-modeling preference inference.
- **Datasets Used**: Over 13,000 risky decisions from Bourgin et al. (2019) plus 47 preference-inference observations from Jern et al. (2017).
- **Results**: GPT-4o, GPT-4-Turbo, Claude 3 Opus, and Llama-3 models align more with expected-value theory than with actual human behavior.
- **Code Available**: Not identified in this pass.
- **Relevance to Our Research**: Critical negative result. A theory of simulation must explicitly model distortions toward rationalized, cleaned-up humans.

### Towards Real-world Human Behavior Simulation: Benchmarking Large Language Models on Long-horizon, Cross-scenario, Heterogeneous Behavior Traces (2026-04-09)
- **Authors**: Chen et al.
- **Source**: arXiv 2604.08362
- **Key Contribution**: Most comprehensive benchmark found here for real-world behavior simulation.
- **Methodology**: OmniBehavior benchmark built from anonymized Kuaishou logs across five scenarios and 22 actions over roughly three months.
- **Datasets Used**: Real-world platform logs; release promised after formal audit.
- **Results**: Current LLMs plateau even with longer context and show hyper-activity, persona homogenization, and utopian bias.
- **Code Available**: Repo/page referenced in paper, but not validated in this pass.
- **Relevance to Our Research**: Strong evidence that single-scenario benchmarks are insufficient for a simulation theory.

## Common Methodologies

- **Prompted human simulation**: Used in Turing Experiments and OpinionQA-style probing.
- **Agent architectures with memory and planning**: Used in Generative Agents and Concordia-style systems.
- **Game-theoretic behavioral tasks**: Used in the trust paper and Turing Experiment replications.
- **Population-alignment evaluation**: Used in OpinionQA and should be central for any superset-of-outcomes claim.

## Standard Baselines

- **Average-human baseline**: Compare against aggregate human distributions rather than only exemplar responses.
- **Demographic-group baseline**: Compare against subgroup distributions, not just overall population.
- **Classical theory baseline**: Expected value theory or simple rational actor models for decision tasks.
- **Ablated simulator baseline**: No-memory / no-reflection / no-persona versions of agent simulators.

## Evaluation Metrics

- **Distribution alignment**: Jensen-Shannon divergence, KL where appropriate, total variation, or exact metrics from OpinionQA.
- **Choice prediction**: Accuracy and macro-F1 on discrete behavioral decisions.
- **Calibration**: Brier score or log loss for predicted human outcome distributions.
- **Diversity preservation**: Entropy, subgroup coverage, and long-tail recall.
- **Trajectory realism**: Sequence-level match for long-horizon settings, including action-frequency and transition statistics.

## Datasets in the Literature

- **OpinionQA**: Best available demographic-opinion alignment benchmark in this pass.
- **Social IQa**: Useful for local social-choice prediction but limited for full simulation.
- **Synthetic-Persona-Chat / Persona-style corpora**: Useful for conditioning and factor extraction, not for realism claims by themselves.
- **Trust Game and classic psychology stimuli**: Strong for targeted fidelity tests.
- **OmniBehavior**: Most promising real-world benchmark, but full public release may lag the paper.

## Gaps and Opportunities

1. **Average-person collapse**
   - Many systems simulate a coherent, prosocial, rationalized “average person” rather than the empirical human distribution.

2. **Weak latent-factor grounding**
   - Persona prompts and trait labels often control style more than causal behavior. A theory of simulation needs latent factors that predict action distributions, not just wording.

3. **Single-task validity does not transfer**
   - Passing a trust benchmark or an opinion benchmark does not imply broad human simulation competence.

4. **Long-horizon structure is under-tested**
   - Most public benchmarks remain short-context, single-scenario, or survey-based.

## Recommendations for Our Experiment

- **Recommended datasets**: Use `OpinionQA` as the primary population-alignment benchmark, `social_i_qa` for scenario-level behavioral choice prediction, and `Synthetic-Persona-Chat` only as auxiliary conditioning data.
- **Recommended baselines**: Unconditioned LLM, persona-conditioned LLM, demographic-conditioned LLM, expected-value or simple rational actor baselines on decision tasks, and a memory-enabled simulator such as Concordia or Generative Agents.
- **Recommended metrics**: Group-level distribution alignment, macro accuracy on discrete choices, calibration, and diversity-preservation metrics that detect homogenization.
- **Methodological considerations**: A theory of simulation should distinguish at least three claims: surface plausibility, latent-factor capture, and distributional coverage. The strongest claim here is not “LLMs simulate humans,” but “LLMs can simulate some human behavioral manifolds under specific prompts and task structures, while systematically distorting variance, tails, and cross-scenario continuity.”
