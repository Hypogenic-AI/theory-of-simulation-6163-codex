# REPORT: A Theory of Simulation

## 1. Executive Summary
This project asked what a theory of simulation should look like for LLMs, and whether a modern LLM can simulate a superset of human outcomes once it is conditioned on latent human factors. I operationalized simulation as three requirements: fidelity to known human-style judgments, responsiveness to latent factors such as persona or demographics, and coverage of plausible outcome variation.

Using real API calls to `gpt-4.1` on May 5, 2026, I ran two experiments: a social-judgment fidelity test on Social IQA and a Turing-Experiment-style ultimatum-game simulation with multiple synthetic participants. The main result is that `gpt-4.1` acts like a structured but biased simulator. Persona conditioning improved Social IQA accuracy from 0.744 to 0.789 and increased the number of distinct ultimatum policies from 2 to 5, but all conditions still accepted unfair offers at unrealistically high rates. The model therefore expands the space of plausible behaviors somewhat, but it does not simulate a true superset of human outcomes; it still compresses behavior toward cooperative, compliant, and rationalized responses.

Practical implication: LLMs are useful as controllable simulators of behavioral manifolds, but not as drop-in substitutes for human populations. A defensible theory of simulation for LLMs should treat them as biased generators whose validity must be established separately for fidelity, subgroup structure, and tail coverage.

## 2. Research Question & Motivation
### Research Question
What would a theory of simulation look like for LLMs, and do modern LLMs simulate a superset of human behavioral outcomes when conditioned on latent factors?

### Why This Matters
Product teams, evaluation pipelines, and agent designers increasingly use LLMs as stand-ins for people. If these models only reproduce an “average, cleaned-up human,” they will systematically underrepresent disagreement, irrationality, and subgroup heterogeneity.

### Literature Gap
The local review in `literature_review.md` shows that prior work demonstrates partial simulation ability, but usually on one task at a time. It also highlights repeated distortions: average-person collapse, rationality bias, and weak latent-factor grounding. The missing piece is a framework that distinguishes believable text generation from distributionally valid human simulation.

## 3. Experimental Setup
### Model and API
- Primary model: `gpt-4.1`
- Endpoint: `v1/chat/completions`
- Date run: 2026-05-05
- Social IQA parameters: `temperature=0.8`, `max_completion_tokens=120`
- Ultimatum parameters: `temperature=0.9`, `max_completion_tokens=120`
- Seeds: deterministic integer seeds generated per condition/item or participant/offer in [src/run_experiments.py](/workspaces/theory-of-simulation-6163-codex/src/run_experiments.py:1)

### Datasets and Tasks
- Social IQA: 90 validation examples sampled in a roughly label-balanced way from `datasets/social_i_qa`
- Persona source: 15 concise persona profiles sampled from `datasets/synthetic_persona_chat`
- Ultimatum game: custom prompt scaffold adapted from the local Turing Experiments assets in `code/turing_experiments/data/prompt-templates/ultimatum_game/`

### Conditions
- `unconditioned`: generic plausible US adult participant
- `demographic`: four demographic role prompts cycled across participants
- `persona`: sampled persona profiles with 4 short stable traits each

### Metrics
- Social IQA: accuracy, macro-F1, answer entropy, exact paired condition comparisons
- Ultimatum game: acceptance curve, inferred acceptance threshold, policy entropy, monotonicity violations, distinct policy profiles
- Cost tracking: prompt tokens, completion tokens, estimated API cost

### Environment
- Workspace: `/workspaces/theory-of-simulation-6163-codex`
- Python: 3.12.8
- Key libraries: `openai 2.34.0`, `datasets 4.8.5`, `numpy 2.4.4`, `pandas 3.0.2`, `scipy 1.17.1`, `scikit-learn 1.8.0`, `matplotlib 3.10.9`, `seaborn 0.13.2`
- GPU detection at session start: 4 × NVIDIA RTX A6000, each with 49,140 MiB total memory. GPU was not used because all experiments were API-based.

### Reproducibility
- Planning: [planning.md](/workspaces/theory-of-simulation-6163-codex/planning.md:1)
- Experiment runner: [src/run_experiments.py](/workspaces/theory-of-simulation-6163-codex/src/run_experiments.py:1)
- Analysis: [src/analyze_results.py](/workspaces/theory-of-simulation-6163-codex/src/analyze_results.py:1)
- Raw outputs: `results/raw/`
- Summaries: `results/summary/`
- Figures: `figures/`

## 4. Results
### 4.1 Social IQA: Human-style local judgment fidelity

| Condition | N | Accuracy | 95% CI | Macro-F1 | Answer entropy (bits) |
|---|---:|---:|---:|---:|---:|
| Demographic | 90 | 0.700 | [0.600, 0.778] | 0.701 | 1.583 |
| Persona | 90 | 0.789 | [0.700, 0.867] | 0.789 | 1.583 |
| Unconditioned | 90 | 0.744 | [0.644, 0.822] | 0.744 | 1.581 |

Key paired comparisons:
- Persona vs Demographic: accuracy delta `+0.089`, exact paired-test proxy `p=0.0215`
- Unconditioned vs Demographic: accuracy delta `+0.044`, `p=0.2188`
- Persona vs Unconditioned: accuracy delta `+0.044`, `p=0.2891`

Interpretation:
- Persona conditioning helped rather than harmed local social reasoning.
- Answer-distribution JS divergences were tiny (`0.0004` to `0.0022`), so conditioning did not radically change the aggregate choice distribution on this benchmark.

### 4.2 Ultimatum Game: Distributional behavioral simulation

| Condition | Participants | Mean threshold | 95% CI | Threshold SD | Policy entropy | Monotonicity violations | Distinct policy profiles |
|---|---:|---:|---:|---:|---:|---:|---:|
| Demographic | 15 | 2.40 | [2.13, 2.67] | 0.51 | 0.608 | 0.000 | 2 |
| Persona | 15 | 2.53 | [1.93, 3.00] | 1.13 | 0.590 | 0.067 | 5 |
| Unconditioned | 15 | 2.67 | [2.40, 2.87] | 0.49 | 0.677 | 0.000 | 2 |

Acceptance rates by offer:

| Offer | Demographic | Persona | Unconditioned |
|---:|---:|---:|---:|
| 1 | 0.000 | 0.267 | 0.000 |
| 2 | 0.600 | 0.333 | 0.333 |
| 3 | 1.000 | 0.800 | 1.000 |
| 4-9 | 1.000 | 1.000 | 1.000 |

Threshold mean differences:
- Unconditioned minus Demographic: `+0.267`, 95% CI `[0.178, 0.351]`
- Persona minus Demographic: `+0.133`, 95% CI `[-0.022, 0.293]`
- Unconditioned minus Persona: `+0.133`, 95% CI `[-0.018, 0.290]`

Distinct policy profiles observed:
- Demographic: `RAAAAAAAA`, `RRAAAAAAA`
- Unconditioned: `RAAAAAAAA`, `RRAAAAAAA`
- Persona: `AAAAAAAAA`, `ARAAAAAAA`, `RAAAAAAAA`, `RRAAAAAAA`, `RRRAAAAAA`

Interpretation:
- All conditions were monotone or nearly monotone, which is good.
- But all conditions accepted unfair offers very early.
- Persona conditioning produced more behavioral variety, including one participant who accepted every offer, but the entire family of policies still concentrated on low acceptance thresholds.

### 4.3 Token Usage and Estimated Cost
Token totals:
- Social IQA: `44,853` prompt + `7,671` completion = `52,524` total
- Ultimatum game: `61,884` prompt + `11,449` completion = `73,333` total
- Overall: `106,737` prompt + `19,120` completion = `125,857` total

Estimated cost:
- Social IQA: about `$0.151`
- Ultimatum game: about `$0.215`
- Overall: about `$0.366`

Estimate basis:
- Official OpenAI pricing checked on 2026-05-05: `gpt-4.1` input `$2.00 / 1M` tokens and output `$8.00 / 1M` tokens
- Sources: https://platform.openai.com/docs/models/gpt-4.1 and https://openai.com/api/pricing

### 4.4 Output Artifacts
- Social IQA raw outputs: `results/raw/social_iqa_gpt-4.1.jsonl`
- Ultimatum raw outputs: `results/raw/ultimatum_gpt-4.1.jsonl`
- Summary table: `results/summary/summary_gpt-4.1.csv`
- Analysis details: `results/summary/analysis_gpt-4.1.json`
- Social IQA figure: `figures/social_iqa_distribution_gpt-4.1.png`
- Ultimatum figure: `figures/ultimatum_curves_gpt-4.1.png`

## 5. Analysis & Discussion
### 5.1 What the Results Show
The results support a middle position. `gpt-4.1` is not merely parroting one average answer, because persona conditioning measurably improved Social IQA accuracy and expanded the set of ultimatum policies. At the same time, the model did not produce evidence of true superset coverage. The added diversity remained narrow and highly structured, and the ultimatum task showed heavy collapse toward early acceptance.

### 5.2 Implications for a Theory of Simulation
The experiments suggest that an LLM simulation theory should separate three layers:

1. Surface plausibility  
The model easily produces coherent human-like justifications.

2. Local fidelity  
The model can align reasonably well with benchmarked social judgments, especially under persona conditioning.

3. Distributional coverage  
This is where the model remains weak. It broadens outcomes somewhat, but not enough to claim coverage of the human tail distribution.

That is the main theoretical answer to the user’s question. If LLMs capture some latent factors behind behavior, they can simulate a wider manifold of outcomes than a single “average human” prompt. But the manifold is still biased and compressed. It is better described as a structured approximation to human outcome space than as a genuine superset.

### 5.3 Error Analysis
Social IQA failures followed a consistent pattern:
- The model often chose an affective state when the benchmark wanted a trait label.
- It often preferred a generally plausible answer over the benchmark’s more specific social inference.
- Examples: choosing “excited” instead of “confident and outgoing,” or “annoying” instead of “being mean.”

Ultimatum failures were more structural:
- Acceptance thresholds were unrealistically low.
- Most participants accepted by offer 2 or 3.
- Demographic prompts barely changed policy families.
- Persona prompts increased variety, but mainly by adding a few even more compliant or slightly stricter profiles.

### 5.4 Relation to Prior Work
These results match the local literature review closely:
- They agree with work showing that LLMs can reproduce some human-style findings under prompting.
- They also agree with the rationality-bias critique: the model behaves like a cooperative, utility-preserving participant rather than a messy human population.
- The findings are also consistent with the “average-person collapse” concern, with persona prompts partially mitigating but not eliminating it.

## 6. Limitations
- Only one current model family was tested.
- Social IQA is likely contaminated by pretraining exposure and is not a pure human-simulation benchmark.
- The local OpinionQA mirror lacked the full human-response tables, so I could not run the strongest available subgroup-distribution evaluation.
- The ultimatum task used a lightweight prompt design rather than a full BDI-style trust or memory architecture.
- Sample size for simulated ultimatum participants was modest at 15 per condition.
- API behavior can drift over time; this run reflects `gpt-4.1` as accessed on 2026-05-05.

## 7. Conclusions & Next Steps
The answer to the research question is no, not in the strong sense. `gpt-4.1` does not simulate a true superset of human outcomes. It simulates a controllable but compressed behavioral manifold: coherent, somewhat responsive to latent factors, but still skewed toward rationalized and compliant behavior.

A viable theory of simulation for LLMs should therefore define success as conditional and task-specific. An LLM can be a useful simulator if it passes fidelity checks, shows meaningful latent-factor responsiveness, and preserves long-tail coverage on the target domain. Current frontier models appear to satisfy the first two conditions more often than the third.

Recommended follow-up work:
- Restore full OpinionQA human-response data and evaluate subgroup alignment directly.
- Add a second current model family such as GPT-5 or Claude Sonnet 4.5 for cross-model comparison.
- Test richer agent architectures using Concordia or the local trust-game scaffolds.
- Move from single-step games to long-horizon benchmarks to test whether diversity persists over time.

## References
- `literature_review.md`
- Park et al. (2023), *Generative Agents: Interactive Simulacra of Human Behavior*
- Aher et al. (2023), *Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies*
- Santurkar et al. (2023), *Whose Opinions Do Language Models Reflect?*
- Lin (2024), *Large language models as linguistic simulators and cognitive models in human research*
- Xie et al. (2024), *Can Large Language Model Agents Simulate Human Trust Behavior?*
- Liu et al. (2025), *Large Language Models Assume People are More Rational than We Really Are*
- Chen et al. (2026), *Towards Real-world Human Behavior Simulation: OmniBehavior*
- OpenAI API model page for GPT-4.1: https://platform.openai.com/docs/models/gpt-4.1
- OpenAI API pricing page: https://openai.com/api/pricing
