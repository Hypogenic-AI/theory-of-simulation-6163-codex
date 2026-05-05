# Planning: A Theory of Simulation for LLMs

## Motivation & Novelty Assessment

### Why This Research Matters
LLMs are increasingly used as stand-ins for people in evaluation, product research, social simulation, and agent design. If these models only reproduce an averaged, rationalized caricature of human behavior, then downstream decisions based on them will systematically miss tails, subgroups, and failure modes that matter most in real settings.

### Gap in Existing Work
The literature in [literature_review.md](/workspaces/theory-of-simulation-6163-codex/literature_review.md:1) shows three recurring gaps: most studies validate LLMs on one narrow task at a time, latent factors such as persona or demographics are often treated as stylistic controls rather than causal behavioral variables, and successful simulations still exhibit rationality, prosociality, or homogenization biases. Existing work therefore does not establish whether LLMs simulate a human distribution, only whether they can imitate selected slices of it.

### Our Novel Contribution
This project operationalizes a theory of simulation as a three-part requirement: fidelity to known human regularities, latent-factor responsiveness, and coverage of plausible outcome variation. We test the specific claim that LLMs can simulate a superset of human outcomes by asking a stricter question: does latent-factor conditioning expand behavioral coverage while preserving empirical structure, or does it merely create broader but less human-like variance?

### Experiment Justification
- Experiment 1: Social IQA fidelity test. Needed to measure whether latent conditioning helps or harms local human-style social judgment on a benchmark with labeled answers.
- Experiment 2: Ultimatum-game simulation test. Needed to evaluate distributional behavior, not just point accuracy, using a classic Turing-Experiment style setup with known human regularities.
- Experiment 3: Coverage and separability analysis across conditions. Needed to test the “superset of outcomes” hypothesis directly by quantifying entropy, unique behavior profiles, and subgroup differentiation.

## Research Question
What would a theory of simulation look like for LLMs, and do modern LLMs simulate a superset of human behavioral outcomes when conditioned on latent human factors such as persona or demographics?

## Background and Motivation
The pre-gathered review suggests that LLM simulation should not be treated as a binary capability. Prior work shows partial success on isolated human-subject replications, opinion reflection, and trust-game behavior, but also consistent distortions such as average-person collapse and over-rationalization. This project tests a narrower and more defensible claim: a useful theory of LLM simulation should explain when models preserve human behavioral structure and when they systematically over- or under-cover the human outcome space.

## Hypothesis Decomposition
- H1: On a local social-judgment benchmark, an unconditioned strong LLM will achieve moderate-to-high fidelity to human-labeled responses.
- H2: Adding latent-factor conditioning will increase behavioral diversity and subgroup separability relative to an unconditioned simulator.
- H3: The diversity gain from latent-factor conditioning will come with a tradeoff: higher coverage but lower average fidelity on canonical labels or known human regularities.
- H4: Therefore, current LLMs are more likely to simulate an expanded manifold of plausible outcomes than a true superset of human outcomes; the expansion will be structured but biased.

Independent variables:
- Prompt condition: unconditioned, demographic-conditioned, persona-conditioned
- Task family: Social IQA, ultimatum game
- Sampling replicate / synthetic participant

Dependent variables:
- Social IQA accuracy and macro-F1
- Ultimatum acceptance rate by offer, monotonicity, and threshold dispersion
- Entropy, support coverage, and pairwise distribution distance across simulated groups

Alternative explanations:
- Prompt complexity may reduce task performance independently of latent-factor modeling
- Higher diversity may reflect noise rather than meaningful subgroup structure
- API model stochasticity may drive variance without reflecting a coherent simulator

## Proposed Methodology

### Approach
Use one real frontier API model as the primary simulator and compare prompt conditions rather than model families. This isolates the role of latent-factor conditioning while keeping model capacity fixed. The methodology combines a labeled social benchmark with a distributional economic-game benchmark because simulation theory must explain both local judgments and population-level behavioral distributions.

### Experimental Steps
1. Inspect and validate local datasets and prompt assets from `datasets/` and `code/turing_experiments/`.
2. Build a reproducible API evaluation harness with cached raw outputs, fixed seeds where supported, and structured JSON parsing.
3. Run Social IQA under three prompt conditions on a stratified subset large enough for statistical comparison.
4. Run an ultimatum-game simulation using multiple synthetic participants and varying offers under the same three conditions.
5. Compute fidelity, diversity, and coverage metrics; test pairwise differences with bootstrap confidence intervals and paired tests where appropriate.
6. Perform error analysis to determine whether broader coverage reflects meaningful latent variation or degraded behavioral realism.

### Baselines
- Unconditioned simulator baseline
- Demographic-conditioned simulator baseline
- Persona-conditioned simulator baseline using concise profiles derived from local persona data
- Historical literature baselines from `turing_experiments` and `agent_trust` for contextual comparison only

### Evaluation Metrics
- Social IQA: accuracy, macro-F1, answer entropy, option-distribution JS divergence across prompt conditions
- Ultimatum game: acceptance rate curve by offer, monotonicity violations, inferred acceptance-threshold mean/std, participant-level entropy
- Coverage metrics: number of distinct policy profiles, average pairwise Jensen-Shannon divergence, long-tail action frequency
- Statistical reporting: bootstrap 95% confidence intervals, McNemar test for paired Social IQA differences where applicable, permutation or bootstrap tests for diversity metrics

### Statistical Analysis Plan
- Significance level: 0.05, two-sided
- Social IQA condition comparisons: paired bootstrap on item accuracy deltas and McNemar tests
- Ultimatum metrics: bootstrap confidence intervals on acceptance curves and threshold summaries
- Effect sizes: mean difference, Cliff's delta where useful, and standardized difference for continuous metrics
- Multiple comparisons: Holm correction within each benchmark family

## Expected Outcomes
Results would support the hypothesis if latent conditioning increases entropy, support coverage, and subgroup separation while preserving at least some core human-regularity structure. Results would refute the hypothesis if conditioning only adds random noise, destroys benchmark fidelity, or fails to produce meaningful distributional broadening.

## Timeline and Milestones
1. Planning and environment verification: complete first
2. Implementation and dataset validation: immediate next step
3. API experiments on Social IQA and ultimatum game: after harness validation
4. Analysis, figures, and statistical testing: after raw outputs are complete
5. Reporting and reproducibility validation: final phase

## Potential Challenges
- The local OpinionQA mirror lacks full human-response tables, so it cannot serve as the primary quantitative representativeness benchmark.
- API availability or parsing failures may require robust retries and caching.
- Persona conditioning can accidentally inject task-irrelevant noise rather than genuine latent-factor variation.
- Human ground truth for the ultimatum game is literature-based rather than locally tabulated, so claims there must remain modest.

Mitigations:
- Use Social IQA and Turing-Experiment assets as the core quantitative benchmarks.
- Save every raw API response and parse with validation plus fallback retries.
- Keep persona prompts short and behaviorally oriented.
- Frame ultimatum results as replication of known regularities plus diversity analysis, not as a full human-distribution estimate.

## Success Criteria
- A reproducible evaluation harness runs end-to-end with real API calls and cached outputs.
- At least two benchmark families are completed with actual results.
- The report can answer the research question with evidence about fidelity, latent-factor responsiveness, and coverage.
- The final conclusion is specific about whether current LLM simulation is average-human mimicry, structured manifold simulation, or genuine superset coverage.
