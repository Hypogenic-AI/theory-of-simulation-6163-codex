# A Theory of Simulation

This project tests a narrow, empirical version of the question: if an LLM captures some latent factors behind human behavior, does conditioning on those factors let it simulate a superset of human outcomes? The study uses real `gpt-4.1` API calls on a social-judgment benchmark and a Turing-Experiment-style ultimatum game.

Key findings:
- `gpt-4.1` behaved like a structured but biased simulator, not a full superset simulator.
- Persona conditioning improved Social IQA accuracy from `0.744` to `0.789`.
- Persona conditioning also increased ultimatum policy diversity from `2` to `5` distinct policies.
- All conditions still accepted unfair offers too easily, indicating rationality/compliance bias and weak tail coverage.
- Total measured usage was `125,857` tokens, with an estimated run cost of about `$0.37`.

Full report: [REPORT.md](/workspaces/theory-of-simulation-6163-codex/REPORT.md:1)

## Reproduce
Set up the isolated environment and run:

```bash
source .venv/bin/activate
python src/run_experiments.py --model gpt-4.1 --social-items 90 --participants 15 --seed 42
python src/analyze_results.py --model gpt-4.1
```

Environment management is in `pyproject.toml`, and dependencies were installed with `uv add`.

## File Structure
- `planning.md`: study design and motivation
- `REPORT.md`: final write-up with results and interpretation
- `literature_review.md`: synthesized related work
- `resources.md`: local datasets, papers, and code inventory
- `src/`: experiment and analysis scripts
- `results/raw/`: raw JSONL model outputs and metadata
- `results/summary/`: computed tables and analysis JSON
- `figures/`: generated plots

## Notes
- GPU was detected at session start but not used because the experiments were API-based.
- The strongest missing benchmark piece is full `OpinionQA` human-response data; the local mirror did not include those tables.
