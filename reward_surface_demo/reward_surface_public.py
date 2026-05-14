#!/usr/bin/env python3
"""Public soft-touch reward-surface demo.

This script visualizes the reward-shaping logic used for a low-dimensional
soft-touch simulation platform. It is a public, self-contained demonstration:
it does not train a policy, run MuJoCo, load private traces, or expose internal
experiment logs.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class RewardConfig:
    """Reward parameters for public visualization."""

    target_force_n: float = 3.0
    preferred_force_sigma_n: float = 2.0
    contact_gap_m: float = 0.004
    contact_gap_sigma_m: float = 0.002
    approach_sigma_m: float = 0.055
    hard_force_start_n: float = 10.0
    hard_force_scale_n: float = 2.0
    speed_penalty_weight: float = 0.45
    smoothness_penalty_weight: float = 0.08
    max_stability_bonus: float = 0.8


def sigmoid(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-x))


def contact_gate(surface_gap_m: np.ndarray, cfg: RewardConfig) -> np.ndarray:
    """Soft gate for being close enough to the target surface."""

    return 1.0 / (
        1.0
        + np.exp((surface_gap_m - cfg.contact_gap_m) / cfg.contact_gap_sigma_m)
    )


def soft_touch_reward(
    surface_gap_m: np.ndarray,
    force_n: np.ndarray,
    approach_speed_mps: float = 0.05,
    stable_steps: int = 8,
    action_delta_norm: float = 0.3,
    cfg: RewardConfig | None = None,
) -> np.ndarray:
    """Compute a public reward surface for soft-touch behavior.

    Positive reward is assigned to near-surface, low-force, stable contact.
    Hard impact, high approach speed, and jerky actions are penalized.
    """

    cfg = cfg or RewardConfig()
    gate = contact_gate(surface_gap_m, cfg)

    approach_reward = 0.9 * np.exp(-np.square(surface_gap_m / cfg.approach_sigma_m))

    preferred_force = np.exp(
        -np.square((force_n - cfg.target_force_n) / cfg.preferred_force_sigma_n)
    )
    soft_contact_reward = 2.4 * gate * preferred_force

    stable_fraction = min(max(stable_steps, 0), 40) / 40.0
    stability_bonus = cfg.max_stability_bonus * stable_fraction * gate * preferred_force

    hard_force_penalty = 2.8 * sigmoid(
        (force_n - cfg.hard_force_start_n) / cfg.hard_force_scale_n
    )
    no_contact_force_penalty = 0.25 * (1.0 - gate) * sigmoid(force_n - 1.0)
    speed_penalty = cfg.speed_penalty_weight * approach_speed_mps**2
    smoothness_penalty = cfg.smoothness_penalty_weight * action_delta_norm**2

    return (
        approach_reward
        + soft_contact_reward
        + stability_bonus
        - hard_force_penalty
        - no_contact_force_penalty
        - speed_penalty
        - smoothness_penalty
    )


def build_surface(cfg: RewardConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    gap_m = np.linspace(0.0, 0.12, 180)
    force_n = np.linspace(0.0, 24.0, 180)
    gap_grid, force_grid = np.meshgrid(gap_m, force_n)
    reward_grid = soft_touch_reward(gap_grid, force_grid, cfg=cfg)
    return gap_grid, force_grid, reward_grid


def save_reward_surface(output: Path, cfg: RewardConfig) -> None:
    gap_grid, force_grid, reward_grid = build_surface(cfg)

    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6.4), dpi=160)
    mesh = ax.contourf(
        gap_grid * 1000.0,
        force_grid,
        reward_grid,
        levels=36,
        cmap="viridis",
    )
    contours = ax.contour(
        gap_grid * 1000.0,
        force_grid,
        reward_grid,
        levels=[0.0, 1.0, 2.0],
        colors="white",
        linewidths=0.8,
        alpha=0.7,
    )
    ax.clabel(contours, inline=True, fontsize=8, fmt="reward %.1f")

    ax.axhline(cfg.target_force_n, color="white", linestyle="--", linewidth=1.0)
    ax.axhline(cfg.hard_force_start_n, color="#ffcc66", linestyle=":", linewidth=1.2)
    ax.axvline(cfg.contact_gap_m * 1000.0, color="white", linestyle="--", linewidth=1.0)

    ax.set_title("Public Soft-Touch Reward Surface Demo")
    ax.set_xlabel("surface gap to target (mm)")
    ax.set_ylabel("first-contact / contact force (N)")
    ax.text(
        7,
        cfg.target_force_n + 0.6,
        "preferred soft-touch band",
        color="white",
        fontsize=9,
    )
    ax.text(
        62,
        cfg.hard_force_start_n + 0.7,
        "hard-impact penalty region",
        color="#ffec99",
        fontsize=9,
    )
    cbar = fig.colorbar(mesh, ax=ax)
    cbar.set_label("reward")

    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("figures/reward_surface_public_demo.png"),
        help="Output path for the generated reward surface figure.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    save_reward_surface(args.output, RewardConfig())
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
