"""Run real-model experiments for the simulation-theory study."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiment_utils import (
    RAW_DIR,
    ROOT,
    build_all_participants,
    call_llm_json,
    ensure_dirs,
    get_client,
    load_social_iqa_subset,
    participant_to_dict,
    save_jsonl,
    save_run_metadata,
    set_seed,
)


SOCIAL_SYSTEM_PROMPT = (
    "You are simulating a human participant for a behavioral study. "
    "Respond as the participant would, not as an assistant, expert, or ethicist. "
    "Return strict JSON with keys answer and reason."
)

ULTIMATUM_SYSTEM_PROMPT = (
    "You are simulating a human participant in a behavioral economics study. "
    "Decide whether the participant accepts or rejects the offer. "
    "Return strict JSON with keys decision and reason."
)


def build_social_messages(participant: dict, item: dict) -> list[dict[str, str]]:
    """Build Social IQA prompt messages."""
    user_prompt = f"""
{participant["descriptor"]}

Task: Read the situation and answer as this participant would.

Context: {item["context"]}
Question: {item["question"]}
Options:
A. {item["choices"]["A"]}
B. {item["choices"]["B"]}
C. {item["choices"]["C"]}

Choose exactly one option.
Return JSON:
{{
  "answer": "A or B or C",
  "reason": "one short sentence"
}}
""".strip()
    return [
        {"role": "system", "content": SOCIAL_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def build_ultimatum_messages(participant: dict, offer: int, total: int = 10) -> list[dict[str, str]]:
    """Build ultimatum-game prompt messages."""
    keep = total - offer
    user_prompt = f"""
{participant["descriptor"]}

Task: Simulate whether this participant accepts or rejects the offer below.

Scenario:
Another player receives ${total}. They keep ${keep} for themselves and offer ${offer} to you.
If you accept, you get ${offer} and the other player keeps ${keep}.
If you reject, both of you get $0.

Return JSON:
{{
  "decision": "accept or reject",
  "reason": "one short sentence"
}}
""".strip()
    return [
        {"role": "system", "content": ULTIMATUM_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def run_social_iqa(model: str, n_items: int, n_participants: int, seed: int) -> Path:
    """Run Social IQA across all prompt conditions."""
    client = get_client()
    items = load_social_iqa_subset(n=n_items, seed=seed)
    participants = build_all_participants(n=n_participants, seed=seed)
    records = []

    for condition_idx, condition in enumerate(["unconditioned", "demographic", "persona"]):
        pool = [p for p in participants if p.condition == condition]
        for item_idx, item in enumerate(items):
            participant = participant_to_dict(pool[item_idx % len(pool)])
            response = call_llm_json(
                client,
                model=model,
                messages=build_social_messages(participant, item),
                temperature=0.8,
                max_tokens=120,
                seed=seed + 1000 * condition_idx + item_idx,
                cache_namespace="social_iqa",
            )
            parsed = response["response"]
            answer = str(parsed.get("answer", "")).strip().upper()
            if answer not in {"A", "B", "C"}:
                answer = "INVALID"
            records.append(
                {
                    "benchmark": "social_iqa",
                    "model": model,
                    "condition": condition,
                    "participant": participant,
                    "item": item,
                    "prediction": answer,
                    "correct": answer == item["gold"],
                    "reason": parsed.get("reason", ""),
                    "usage": response["usage"],
                }
            )

    output_path = RAW_DIR / f"social_iqa_{model.replace('/', '_')}.jsonl"
    save_jsonl(records, output_path)
    return output_path


def run_ultimatum(model: str, n_participants: int, seed: int) -> Path:
    """Run ultimatum-game simulations across all prompt conditions."""
    client = get_client()
    participants = build_all_participants(n=n_participants, seed=seed)
    offers = list(range(1, 10))
    records = []

    for condition_idx, condition in enumerate(["unconditioned", "demographic", "persona"]):
        pool = [p for p in participants if p.condition == condition]
        for participant_idx, participant_obj in enumerate(pool):
            participant = participant_to_dict(participant_obj)
            for offer in offers:
                response = call_llm_json(
                    client,
                    model=model,
                    messages=build_ultimatum_messages(participant, offer=offer),
                    temperature=0.9,
                    max_tokens=120,
                    seed=seed + 10000 * condition_idx + 100 * participant_idx + offer,
                    cache_namespace="ultimatum",
                )
                parsed = response["response"]
                decision = str(parsed.get("decision", "")).strip().lower()
                if decision not in {"accept", "reject"}:
                    decision = "invalid"
                records.append(
                    {
                        "benchmark": "ultimatum_game",
                        "model": model,
                        "condition": condition,
                        "participant": participant,
                        "offer": offer,
                        "decision": decision,
                        "accepted": decision == "accept",
                        "reason": parsed.get("reason", ""),
                        "usage": response["usage"],
                    }
                )

    output_path = RAW_DIR / f"ultimatum_{model.replace('/', '_')}.jsonl"
    save_jsonl(records, output_path)
    return output_path


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4.1")
    parser.add_argument("--social-items", type=int, default=90)
    parser.add_argument("--participants", type=int, default=15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    ensure_dirs()
    set_seed(args.seed)

    metadata_path = RAW_DIR / f"run_metadata_{args.model.replace('/', '_')}.json"
    save_run_metadata(
        metadata_path,
        {
            "workspace_root": str(ROOT),
            "model": args.model,
            "social_items": args.social_items,
            "participants_per_condition": args.participants,
            "seed": args.seed,
        },
    )

    social_path = run_social_iqa(
        model=args.model,
        n_items=args.social_items,
        n_participants=args.participants,
        seed=args.seed,
    )
    ultimatum_path = run_ultimatum(
        model=args.model,
        n_participants=args.participants,
        seed=args.seed,
    )

    manifest = {
        "model": args.model,
        "social_iqa_raw": str(social_path),
        "ultimatum_raw": str(ultimatum_path),
        "metadata": str(metadata_path),
    }
    manifest_path = RAW_DIR / f"manifest_{args.model.replace('/', '_')}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
