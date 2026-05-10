#!/usr/bin/env python3
"""Generate a small contact-quality evidence report from redacted metrics."""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path
from typing import Any


def rate(count: int, total: int) -> float:
    return count / total if total else 0.0


def mean(values: list[float]) -> float | None:
    return statistics.fmean(values) if values else None


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * pct
    lower = int(rank)
    upper = min(lower + 1, len(ordered) - 1)
    weight = rank - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def classify_episode(ep: dict[str, Any]) -> str:
    raw = bool(ep.get("raw_contact"))
    valid = bool(ep.get("valid_touch"))
    stable = bool(ep.get("stable_soft_touch"))
    over_force = bool(ep.get("over_force"))
    streak = int(ep.get("max_contact_streak") or 0)
    gap = ep.get("surface_gap_min")

    if stable:
        return "stable_soft_touch"
    if over_force:
        return "hard_contact"
    if valid:
        return "valid_unstable_touch"
    if raw:
        return "raw_contact_only"
    if gap is not None and float(gap) < 0.002:
        return "hover_or_signal_mismatch"
    if streak > 0:
        return "raw_contact_only"
    return "no_contact"


def fmt_rate(value: float) -> str:
    return f"{value * 100:.1f}%"


def fmt_float(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def build_report(payload: dict[str, Any]) -> str:
    episodes = payload.get("episodes", [])
    if not isinstance(episodes, list):
        raise ValueError("input JSON must contain an episodes list")

    total = len(episodes)
    labels = [classify_episode(ep) for ep in episodes]
    counts = {label: labels.count(label) for label in sorted(set(labels))}

    raw_count = sum(1 for ep in episodes if ep.get("raw_contact"))
    valid_count = sum(1 for ep in episodes if ep.get("valid_touch"))
    stable_count = sum(1 for ep in episodes if ep.get("stable_soft_touch"))
    over_force_count = sum(1 for ep in episodes if ep.get("over_force"))

    forces = [
        float(ep["first_contact_force"])
        for ep in episodes
        if ep.get("first_contact_force") is not None
    ]
    speeds = [
        float(ep["first_contact_speed"])
        for ep in episodes
        if ep.get("first_contact_speed") is not None
    ]

    conversion = rate(valid_count, raw_count)
    over_force_among_touch = rate(over_force_count, raw_count)

    if stable_count > 0:
        interpretation = "The sample contains stable soft-touch examples, but aggregate quality still depends on repeatability and force tails."
    elif valid_count > 0:
        interpretation = "The sample reaches valid contact without stable hold; this is a boundary-data signal rather than success."
    elif raw_count > 0:
        interpretation = "The sample is dominated by raw contact without valid touch; loose contact should not be treated as progress."
    else:
        interpretation = "The sample contains no contact evidence."

    lines = [
        "# Soft-Touch Evidence Report",
        "",
        f"Dataset note: {payload.get('dataset_note', 'n/a')}",
        "",
        "## Aggregate Metrics",
        "",
        f"- episodes: {total}",
        f"- touch_rate: {fmt_rate(rate(raw_count, total))}",
        f"- valid_touch_rate: {fmt_rate(rate(valid_count, total))}",
        f"- stable_soft_touch_rate: {fmt_rate(rate(stable_count, total))}",
        f"- over_force_rate: {fmt_rate(rate(over_force_count, total))}",
        f"- raw_to_valid_conversion_rate: {fmt_rate(conversion)}",
        f"- over_force_among_touched: {fmt_rate(over_force_among_touch)}",
        f"- first_contact_force_mean: {fmt_float(mean(forces))}",
        f"- first_contact_force_p90: {fmt_float(percentile(forces, 0.9))}",
        f"- first_contact_speed_mean: {fmt_float(mean(speeds))}",
        f"- first_contact_speed_p90: {fmt_float(percentile(speeds, 0.9))}",
        "",
        "## Episode Labels",
        "",
    ]

    for label in [
        "no_contact",
        "hover_or_signal_mismatch",
        "raw_contact_only",
        "hard_contact",
        "valid_unstable_touch",
        "stable_soft_touch",
    ]:
        lines.append(f"- {label}: {counts.get(label, 0)}")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            interpretation,
            "",
            "This report is diagnostic. It does not claim policy success, real-robot readiness, or completion of the full token control loop.",
            "",
            "## Per-Episode Classification",
            "",
            "| episode_id | label | raw_contact | valid_touch | stable_soft_touch | over_force |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )

    for ep, label in zip(episodes, labels):
        lines.append(
            "| {episode_id} | {label} | {raw} | {valid} | {stable} | {over_force} |".format(
                episode_id=ep.get("episode_id", "unknown"),
                label=label,
                raw=bool(ep.get("raw_contact")),
                valid=bool(ep.get("valid_touch")),
                stable=bool(ep.get("stable_soft_touch")),
                over_force=bool(ep.get("over_force")),
            )
        )

    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: run_demo.py <input_metrics.json> <output_report.md>", file=sys.stderr)
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    report = build_report(payload)
    output_path.write_text(report, encoding="utf-8")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
