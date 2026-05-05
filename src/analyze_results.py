"""Analyze simulation-theory experiment outputs and generate figures."""

from __future__ import annotations

import argparse
import json
from math import log2
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import binomtest, bootstrap
from sklearn.metrics import f1_score

from experiment_utils import FIGURES_DIR, RAW_DIR, SUMMARY_DIR, ensure_dirs, load_jsonl


def entropy_from_counts(counts: pd.Series) -> float:
    """Compute Shannon entropy in bits."""
    total = counts.sum()
    probs = counts[counts > 0] / total
    return float(-(probs * probs.map(log2)).sum())


def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """Compute Jensen-Shannon divergence."""
    p = p / p.sum()
    q = q / q.sum()
    m = 0.5 * (p + q)
    kl_pm = np.sum(np.where(p > 0, p * np.log2(p / m), 0.0))
    kl_qm = np.sum(np.where(q > 0, q * np.log2(q / m), 0.0))
    return float(0.5 * (kl_pm + kl_qm))


def bootstrap_ci_binary(values: np.ndarray) -> tuple[float, float]:
    """Bootstrap CI for mean of binary or bounded values."""
    res = bootstrap((values,), np.mean, confidence_level=0.95, n_resamples=2000, random_state=42)
    return float(res.confidence_interval.low), float(res.confidence_interval.high)


def analyze_social(model: str) -> tuple[pd.DataFrame, dict]:
    """Analyze Social IQA results."""
    records = load_jsonl(RAW_DIR / f"social_iqa_{model.replace('/', '_')}.jsonl")
    df = pd.DataFrame(records)
    labels = ["A", "B", "C"]
    summary_rows = []
    distributions = {}
    for condition, cdf in df.groupby("condition"):
        pred_counts = cdf["prediction"].value_counts().reindex(labels, fill_value=0)
        entropy = entropy_from_counts(pred_counts)
        accuracy = float(cdf["correct"].mean())
        ci_low, ci_high = bootstrap_ci_binary(cdf["correct"].astype(int).to_numpy())
        macro_f1 = f1_score(cdf["item"].map(lambda x: x["gold"]), cdf["prediction"], labels=labels, average="macro")
        summary_rows.append(
            {
                "benchmark": "social_iqa",
                "condition": condition,
                "n": len(cdf),
                "accuracy": accuracy,
                "accuracy_ci_low": ci_low,
                "accuracy_ci_high": ci_high,
                "macro_f1": float(macro_f1),
                "answer_entropy_bits": entropy,
                "invalid_rate": float((cdf["prediction"] == "INVALID").mean()),
            }
        )
        distributions[condition] = pred_counts.to_numpy(dtype=float)
    summary_df = pd.DataFrame(summary_rows).sort_values("condition")

    js_rows = []
    conditions = list(distributions)
    for i, left in enumerate(conditions):
        for right in conditions[i + 1 :]:
            js_rows.append(
                {
                    "left": left,
                    "right": right,
                    "js_divergence": js_divergence(distributions[left], distributions[right]),
                }
            )

    pairwise_tests = []
    wide = df.pivot_table(index=df["item"].map(lambda x: x["item_id"]), columns="condition", values="correct", aggfunc="first")
    for i, left in enumerate(conditions):
        for right in conditions[i + 1 :]:
            discordant_left = int(((wide[left] == 1) & (wide[right] == 0)).sum())
            discordant_right = int(((wide[left] == 0) & (wide[right] == 1)).sum())
            total_discordant = discordant_left + discordant_right
            pvalue = (
                float(binomtest(discordant_left, total_discordant, p=0.5).pvalue)
                if total_discordant
                else 1.0
            )
            pairwise_tests.append(
                {
                    "left": left,
                    "right": right,
                    "left_only_correct": discordant_left,
                    "right_only_correct": discordant_right,
                    "accuracy_delta_right_minus_left": float(wide[right].mean() - wide[left].mean()),
                    "mcnemar_exact_pvalue_proxy": pvalue,
                }
            )

    usage_summary = (
        df.assign(
            prompt_tokens=df["usage"].map(lambda x: x.get("prompt_tokens", 0)),
            completion_tokens=df["usage"].map(lambda x: x.get("completion_tokens", 0)),
            total_tokens=df["usage"].map(lambda x: x.get("total_tokens", 0)),
        )[["condition", "prompt_tokens", "completion_tokens", "total_tokens"]]
        .groupby("condition", as_index=False)
        .sum()
    )

    plot_df = (
        df.groupby(["condition", "prediction"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    plt.figure(figsize=(8, 5))
    sns.barplot(data=plot_df, x="condition", y="count", hue="prediction", order=sorted(df["condition"].unique()))
    plt.title(f"Social IQA answer distribution by condition ({model})")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"social_iqa_distribution_{model.replace('/', '_')}.png", dpi=200)
    plt.close()

    return summary_df, {"pairwise_js": js_rows, "pairwise_tests": pairwise_tests, "usage_summary": usage_summary.to_dict(orient="records")}


def infer_threshold(decisions: list[bool]) -> int:
    """Infer the first accepted offer as the acceptance threshold."""
    for idx, accepted in enumerate(decisions, start=1):
        if accepted:
            return idx
    return 10


def monotonicity_violations(decisions: list[bool]) -> int:
    """Count accept->reject reversals as offer increases."""
    violations = 0
    for left, right in zip(decisions[:-1], decisions[1:]):
        if left and not right:
            violations += 1
    return violations


def analyze_ultimatum(model: str) -> tuple[pd.DataFrame, dict]:
    """Analyze ultimatum-game results."""
    records = load_jsonl(RAW_DIR / f"ultimatum_{model.replace('/', '_')}.jsonl")
    df = pd.DataFrame(records)

    participant_rows = []
    for (condition, participant_id), pdf in df.groupby(
        [df["condition"], df["participant"].map(lambda x: x["participant_id"])]
    ):
        ordered = pdf.sort_values("offer")
        decisions = ordered["accepted"].tolist()
        participant_rows.append(
            {
                "condition": condition,
                "participant_id": participant_id,
                "threshold": infer_threshold(decisions),
                "policy_entropy_bits": entropy_from_counts(pd.Series(decisions).value_counts()),
                "monotonicity_violations": monotonicity_violations(decisions),
                "policy_profile": "".join("A" if x else "R" for x in decisions),
            }
        )
    participant_df = pd.DataFrame(participant_rows)

    summary_rows = []
    for condition, cdf in participant_df.groupby("condition"):
        threshold_ci_low, threshold_ci_high = bootstrap(
            (cdf["threshold"].to_numpy(),),
            np.mean,
            confidence_level=0.95,
            n_resamples=2000,
            random_state=42,
        ).confidence_interval
        summary_rows.append(
            {
                "benchmark": "ultimatum_game",
                "condition": condition,
                "n_participants": len(cdf),
                "mean_threshold": float(cdf["threshold"].mean()),
                "threshold_ci_low": float(threshold_ci_low),
                "threshold_ci_high": float(threshold_ci_high),
                "threshold_std": float(cdf["threshold"].std(ddof=1)),
                "mean_policy_entropy_bits": float(cdf["policy_entropy_bits"].mean()),
                "mean_monotonicity_violations": float(cdf["monotonicity_violations"].mean()),
                "distinct_policy_profiles": int(cdf["policy_profile"].nunique()),
            }
        )
    summary_df = pd.DataFrame(summary_rows).sort_values("condition")

    curve_df = df.groupby(["condition", "offer"], as_index=False)["accepted"].mean()
    threshold_pairwise = []
    conditions = sorted(participant_df["condition"].unique())
    for i, left in enumerate(conditions):
        for right in conditions[i + 1 :]:
            left_values = participant_df[participant_df["condition"] == left]["threshold"].to_numpy()
            right_values = participant_df[participant_df["condition"] == right]["threshold"].to_numpy()
            left_mean = float(left_values.mean()) if len(left_values) else 0.0
            right_mean = float(right_values.mean()) if len(right_values) else 0.0
            combined = np.subtract.outer(right_values, left_values).ravel()
            if len(combined):
                ci = bootstrap((combined,), np.mean, confidence_level=0.95, n_resamples=2000, random_state=42).confidence_interval
                mean_delta = right_mean - left_mean
                low = float(ci.low)
                high = float(ci.high)
            else:
                mean_delta = 0.0
                low = 0.0
                high = 0.0
            threshold_pairwise.append(
                {
                    "left": left,
                    "right": right,
                    "mean_threshold_delta_right_minus_left": mean_delta,
                    "delta_ci_low": low,
                    "delta_ci_high": high,
                }
            )

    usage_summary = (
        df.assign(
            prompt_tokens=df["usage"].map(lambda x: x.get("prompt_tokens", 0)),
            completion_tokens=df["usage"].map(lambda x: x.get("completion_tokens", 0)),
            total_tokens=df["usage"].map(lambda x: x.get("total_tokens", 0)),
        )[["condition", "prompt_tokens", "completion_tokens", "total_tokens"]]
        .groupby("condition", as_index=False)
        .sum()
    )
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=curve_df, x="offer", y="accepted", hue="condition", marker="o")
    plt.title(f"Ultimatum acceptance curves by condition ({model})")
    plt.ylabel("Acceptance rate")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"ultimatum_curves_{model.replace('/', '_')}.png", dpi=200)
    plt.close()

    return summary_df, {"curve_rows": curve_df.to_dict(orient="records"), "threshold_pairwise": threshold_pairwise, "usage_summary": usage_summary.to_dict(orient="records")}


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4.1")
    args = parser.parse_args()

    ensure_dirs()
    social_summary, social_extra = analyze_social(args.model)
    ultimatum_summary, ultimatum_extra = analyze_ultimatum(args.model)

    combined = pd.concat([social_summary, ultimatum_summary], ignore_index=True, sort=False)
    combined.to_csv(SUMMARY_DIR / f"summary_{args.model.replace('/', '_')}.csv", index=False)

    analysis_payload = {
        "social_iqa": social_extra,
        "ultimatum_game": ultimatum_extra,
    }
    (SUMMARY_DIR / f"analysis_{args.model.replace('/', '_')}.json").write_text(
        json.dumps(analysis_payload, indent=2)
    )

    print(combined.to_string(index=False))


if __name__ == "__main__":
    main()
