% Outline for "A Theory of Simulation for Language Models"

## Title
- A Theory of Simulation for Language Models: Persona Conditioning Broadens Behavior but Does Not Recover Human Outcome Tails

## Abstract
- Context: teams increasingly use LLMs as stand-ins for people.
- Gap: prior work shows task-specific simulation success but does not separate local fidelity from distributional coverage.
- Approach: define simulation as fidelity, latent-factor responsiveness, and coverage; test `gpt-4.1` on Social IQA and an ultimatum game under unconditioned, demographic, and persona prompting.
- Key results: persona conditioning raises Social IQA accuracy from 0.744 to 0.789 and increases distinct ultimatum policies from 2 to 5, but all conditions accept unfair offers too early.
- Takeaway: current LLMs are controllable but compressed behavioral simulators, not substitutes for human populations.

## Introduction
- Hook: LLMs are already used as synthetic users and participants.
- Importance: if they collapse to an average, compliant person, downstream evaluations miss subgroup and tail behavior.
- Gap: existing work validates single tasks or style controls, not a general theory of simulation.
- Approach: define three-part theory and test it with one labeled benchmark and one distributional game benchmark.
- Quantitative preview: persona improves Social IQA by 4.4 points over unconditioned and 8.9 over demographic; persona raises policy support from 2 to 5 profiles.
- Contributions:
  - propose a theory of simulation with three requirements;
  - conduct two real-API experiments on `gpt-4.1`;
  - show latent conditioning widens outcomes without covering human tails;
  - argue for validation by fidelity, subgroup structure, and tail coverage separately.

## Related Work
- Theme 1: simulation architectures and believable agents.
  - Park et al. on generative agents.
  - Position: believable interaction is not enough for distributional validity.
- Theme 2: human-study replication and economic-game simulation.
  - Aher et al.; Xie et al.
  - Position: we reuse this evaluation spirit but focus on latent-factor responsiveness and coverage.
- Theme 3: population alignment and representativeness.
  - Santurkar et al.; Lin.
  - Position: we operationalize the conceptual caution into measurable criteria.
- Theme 4: critiques of rationality and average-person collapse.
  - Liu et al.; Chen et al.; personality simulation work.
  - Position: our results provide a compact empirical case study consistent with these critiques.

## Methodology
- Formalize simulation criteria:
  - local fidelity;
  - latent-factor responsiveness;
  - coverage of plausible variation.
- Model and setup:
  - `gpt-4.1`, `v1/chat/completions`, date 2026-05-05.
  - temperatures, token limits, seeded calls.
- Tasks:
  - Social IQA: 90 stratified validation items.
  - Ultimatum: 15 synthetic participants per condition, offers 1--9.
- Conditions:
  - unconditioned, demographic, persona.
- Metrics:
  - Social IQA accuracy, macro-F1, entropy, paired tests, JS divergence.
  - Ultimatum thresholds, entropy, monotonicity, distinct profiles.
- Evidence mapping:
  - Table for Social IQA;
  - Table for ultimatum;
  - Figure for distribution plot;
  - Figure for acceptance curves.

## Results
- Social IQA subsection:
  - persona best accuracy and macro-F1;
  - tiny JS divergence means conditioning did not change aggregate label distribution much;
  - paired improvement over demographic is statistically strongest.
- Ultimatum subsection:
  - all conditions accept by offers 2--3 on average;
  - persona yields highest threshold spread and five profiles;
  - unconditioned has highest mean threshold but still unrealistic early acceptance.
- Efficiency subsection:
  - 125,857 total tokens, about $0.366.
- Transition: coverage broadened, but only within a narrow cooperative policy family.

## Discussion
- Interpretation:
  - persona helps local reasoning and slightly broadens support;
  - no evidence for true superset coverage.
- Theoretical implication:
  - distinguish surface plausibility, local fidelity, and distributional coverage.
- Error analysis:
  - Social IQA: affective state vs trait-label confusions; plausible-but-nonspecific responses.
  - Ultimatum: low thresholds, weak demographic separation, compliant persona variants.
- Limitations:
  - one model family;
  - possible benchmark contamination;
  - no full OpinionQA subgroup tables;
  - modest participant count;
  - API drift.
- Broader implication:
  - use LLMs as controllable generators, not drop-in human substitutes.

## Conclusion
- Restate contributions and answer: no strong superset simulation.
- Key takeaway: current frontier LLMs simulate structured but compressed behavioral manifolds.
- Future work: recover full OpinionQA, compare models, test richer architectures, move to long-horizon tasks.

## Tables and Figures
- `tables/social_iqa_results.tex`
- `tables/ultimatum_results.tex`
- `figures/social_iqa_distribution_gpt-4.1.png`
- `figures/ultimatum_curves_gpt-4.1.png`

## Citation Plan
- Park et al. 2023
- Aher et al. 2023
- Santurkar et al. 2023
- Lin 2025 / arXiv 2024
- Xie et al. 2024
- Sorokovikova et al. 2024
- Liu et al. 2025
- Chen et al. 2026
- OpenAI GPT-4.1 model page
- OpenAI API pricing page
