# Cloned Repositories

## Repo 1: generative_agents
- URL: https://github.com/joonspk-research/generative_agents
- Purpose: Original Smallville simulation environment for Generative Agents.
- Location: `code/generative_agents/`
- Key files: `reverie/backend_server/reverie.py`, `environment/frontend_server/manage.py`, `reverie/compress_sim_storage.py`
- Notes: Requires an OpenAI API key in a hand-created `utils.py`; runs a Django environment server plus a backend simulation server. Heavy but directly relevant to agent memory, planning, and reflection.

## Repo 2: agent_trust
- URL: https://github.com/camel-ai/agent-trust
- Purpose: Trust Game experiments from "Can Large Language Model Agents Simulate Human Trust Behavior?"
- Location: `code/agent_trust/`
- Key files: `agent_trust/all_game_person.py`, `agent_trust/no_repeated_demo.py`, `agent_trust/repeated_demo.py`, `agent_trust/prompt/`
- Notes: Strong benchmark scaffold for behavioral alignment under controlled economic games. Dependencies are Python-heavy but tractable.

## Repo 3: opinions_qa
- URL: https://github.com/tatsu-lab/opinions_qa
- Purpose: Code and data utilities for OpinionQA-based representativeness, steerability, and consistency analysis.
- Location: `code/opinions_qa/`
- Key files: `process_results.ipynb`, `representativeness.ipynb`, `steerability.ipynb`, `consistency.ipynb`
- Notes: Best starting point for quantitative population-alignment evaluation. README expects the OpinionQA data bundle in `./data`.

## Repo 4: turing_experiments
- URL: https://github.com/microsoft/turing-experiments
- Purpose: Replication framework for simulated human subject studies.
- Location: `code/turing_experiments/`
- Key files: `scripts/Simulate_Ultimatum_Game_Experiment.ipynb`, `scripts/Simulate_Garden_Path_Experiment.ipynb`, `scripts/simulate_milgram/`, `scripts/wisdom_of_crowds.ipynb`
- Notes: Includes experiment logic and some data. Full replication requires Git LFS for large result files and API credentials for fresh runs.

## Repo 5: concordia
- URL: https://github.com/google-deepmind/concordia
- Purpose: General-purpose library for generative social simulation.
- Location: `code/concordia/`
- Key files: `examples/tutorial.ipynb`, `concordia/prefabs/`, `concordia/components/`, `concordia/environment/`
- Notes: Most reusable framework in this set for new experiments. Requires an external LLM API and embedding model.

## Validation Notes

- Repositories were cloned successfully.
- I inspected the top-level READMEs and key entry points.
- I did not run full examples because most require external API keys, heavyweight setups, or Git LFS data pulls.
