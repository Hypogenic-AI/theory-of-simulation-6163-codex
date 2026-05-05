"""Utilities for simulation-theory experiments with real LLM API calls."""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from datasets import load_from_disk
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RAW_DIR = RESULTS_DIR / "raw"
SUMMARY_DIR = RESULTS_DIR / "summary"
FIGURES_DIR = ROOT / "figures"
LOGS_DIR = ROOT / "logs"


def ensure_dirs() -> None:
    """Create output directories if they do not already exist."""
    for path in [RESULTS_DIR, RAW_DIR, SUMMARY_DIR, FIGURES_DIR, LOGS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def set_seed(seed: int = 42) -> None:
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)


def get_client() -> OpenAI:
    """Construct an OpenAI client from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def stable_json_dumps(obj: Any) -> str:
    """Serialize JSON deterministically for caching."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=True)


def extract_json_block(text: str) -> dict[str, Any]:
    """Parse JSON from a model response, including fenced output fallback."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


@retry(wait=wait_exponential(min=1, max=30), stop=stop_after_attempt(5))
def call_llm_json(
    client: OpenAI,
    *,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
    seed: int,
    cache_namespace: str,
) -> dict[str, Any]:
    """Call the chat completions API and cache the parsed JSON response."""
    cache_payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "seed": seed,
    }
    cache_key = hashlib.sha256(stable_json_dumps(cache_payload).encode("utf-8")).hexdigest()
    cache_path = RAW_DIR / f"{cache_namespace}_cache_{cache_key}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text())

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        seed=seed,
        response_format={"type": "json_object"},
    )
    content = completion.choices[0].message.content or "{}"
    parsed = {
        "request": cache_payload,
        "response": extract_json_block(content),
        "usage": completion.usage.model_dump() if completion.usage else {},
        "created_at": datetime.utcnow().isoformat(),
    }
    cache_path.write_text(json.dumps(parsed, indent=2))
    return parsed


def save_jsonl(records: list[dict[str, Any]], path: Path) -> None:
    """Save records as JSONL."""
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load JSONL file."""
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


@dataclass
class Participant:
    """Simulation participant description."""

    participant_id: str
    condition: str
    descriptor: str
    group: str


def load_persona_participants(n: int, seed: int = 42) -> list[Participant]:
    """Sample concise persona profiles from the local persona dataset."""
    ds = load_from_disk(str(ROOT / "datasets" / "synthetic_persona_chat"))["train"]
    rng = random.Random(seed)
    indices = rng.sample(range(len(ds)), n)
    participants: list[Participant] = []
    for idx, row_idx in enumerate(indices):
        persona_lines = [
            line.strip()
            for line in ds[row_idx]["user 1 personas"].splitlines()
            if line.strip()
        ][:4]
        descriptor = "Simulate a participant with these stable traits:\n" + "\n".join(
            f"- {line}" for line in persona_lines
        )
        participants.append(
            Participant(
                participant_id=f"persona_{idx:02d}",
                condition="persona",
                descriptor=descriptor,
                group="persona",
            )
        )
    return participants


def build_demographic_participants(n: int) -> list[Participant]:
    """Construct demographic-profile participants."""
    groups = [
        (
            "African American",
            "Simulate an African American adult participant in the United States. "
            "Respond as a plausible person, not as a stereotype.",
        ),
        (
            "Asian American",
            "Simulate an Asian American adult participant in the United States. "
            "Respond as a plausible person, not as a stereotype.",
        ),
        (
            "Latino American",
            "Simulate a Latino American adult participant in the United States. "
            "Respond as a plausible person, not as a stereotype.",
        ),
        (
            "White American",
            "Simulate a White American adult participant in the United States. "
            "Respond as a plausible person, not as a stereotype.",
        ),
    ]
    participants: list[Participant] = []
    for idx in range(n):
        group, descriptor = groups[idx % len(groups)]
        participants.append(
            Participant(
                participant_id=f"demo_{idx:02d}",
                condition="demographic",
                descriptor=descriptor,
                group=group,
            )
        )
    return participants


def build_unconditioned_participants(n: int) -> list[Participant]:
    """Construct generic participants with no latent-factor steering."""
    return [
        Participant(
            participant_id=f"base_{idx:02d}",
            condition="unconditioned",
            descriptor="Simulate one plausible adult human participant in the United States.",
            group="overall",
        )
        for idx in range(n)
    ]


def build_all_participants(n: int, seed: int = 42) -> list[Participant]:
    """Build participant pools for all conditions."""
    return (
        build_unconditioned_participants(n)
        + build_demographic_participants(n)
        + load_persona_participants(n, seed=seed)
    )


def load_social_iqa_subset(n: int, seed: int = 42) -> list[dict[str, Any]]:
    """Load a roughly balanced Social IQA validation subset."""
    ds = load_from_disk(str(ROOT / "datasets" / "social_i_qa"))["validation"]
    grouped: dict[str, list[int]] = {"1": [], "2": [], "3": []}
    for idx, row in enumerate(ds):
        grouped[row["label"]].append(idx)
    rng = random.Random(seed)
    per_label = n // 3
    chosen = []
    for label in ["1", "2", "3"]:
        chosen.extend(rng.sample(grouped[label], per_label))
    rng.shuffle(chosen)
    items: list[dict[str, Any]] = []
    for eval_id, idx in enumerate(chosen):
        row = ds[int(idx)]
        items.append(
            {
                "item_id": f"siqa_{eval_id:03d}",
                "context": row["context"],
                "question": row["question"],
                "choices": {
                    "A": row["answerA"],
                    "B": row["answerB"],
                    "C": row["answerC"],
                },
                "gold": {"1": "A", "2": "B", "3": "C"}[row["label"]],
            }
        )
    return items


def save_run_metadata(path: Path, metadata: dict[str, Any]) -> None:
    """Save run metadata and environment details."""
    payload = {
        **metadata,
        "python": sys.version,
        "timestamp_utc": datetime.utcnow().isoformat(),
    }
    path.write_text(json.dumps(payload, indent=2))


def participant_to_dict(participant: Participant) -> dict[str, Any]:
    """Serialize a participant dataclass."""
    return asdict(participant)
