# Qingmiao Embodied Generalization Showcase

This repository is a public-facing research showcase for an embodied AI project on task-general contact control. The long-term question is how to move from task-specific robot control pipelines toward a unified token-based control loop that can transfer across contact-sensitive tasks.

The current minimum validation task is soft touch in simulation. It is deliberately narrow: the task exposes whether a controller can distinguish loose contact, unsafe contact, valid touch, and stable low-force contact under strict metrics. The repository therefore emphasizes evidence quality, failure taxonomy, and architecture direction rather than claiming a finished robot policy.

This folder is designed as Qingmiao support material. It is small by design: public narrative, clean architecture notes, a runnable evidence-loop demo, and explicit data boundaries. Raw experiment archives, internal audit materials, checkpoints, traces, and platform logs are excluded.

## Core Idea

Traditional robot control often separates perception, state estimation, policy learning, action mapping, and motor execution into a specialized chain. This project explores a more unified route:

```text
sensor / observation tokens
+ latent state z(t) tokens
+ goal and context tokens
        |
        v
DreamerV3-style world model
        |
        v
imagined rollouts and contact dynamics representation
        |
        v
Emu3.5-style next-action-token prediction
        |
        v
safety wrapper and motor execution
```

The key architectural hypothesis is that a learned latent dynamics state `z(t)` should directly condition action-token prediction. Physical regularity and action generation are then coupled inside the same control loop, instead of being handled as disconnected modules.

## What Is Included

- `REPO_NAVIGATION.md`: recommended reading order and repository scope.
- `docs/project_overview.md`: research motivation, current status, and Qingmiao-facing project summary.
- `docs/architecture.md`: full token control loop direction with DreamerV3 and Emu3.5 roles.
- `docs/contact_quality_taxonomy.md`: metric discipline and failure categories for soft-touch validation.
- `docs/roadmap.md`: staged plan from evidence loop to tokenized embodied control.
- `docs/qingmiao_support_note.md`: how this repository supports a Qingmiao-style review.
- `soft_touch_evidence_loop_demo/`: a small runnable demo that classifies redacted sample episodes and generates a Markdown evidence report.
- `data_samples/DATA_AVAILABILITY.md`: what data is public, redacted, or withheld.
- `REPRODUCIBILITY.md`: how to reproduce the public demo on a normal laptop.

## Run The Demo

```bash
cd soft_touch_evidence_loop_demo
python3 run_demo.py sample_metrics.json demo_report.md
```

The demo is not a controller and does not train a policy. It shows how this project treats contact evidence: loose touch is separated from valid touch, over-force contact, unstable contact, and stable soft touch.

## Figure Status

No public architecture figure is included yet. The placeholder in `figures/FIGURE_TODO.md` is intentional; a clean diagram can be added later after the public architecture wording is stable.

## Current Claim Boundary

The current project state is research-in-progress:

- soft-touch is not presented as solved;
- direct Emu3.5 motor control is not presented as implemented;
- the DreamerV3 + Emu3.5 closed-loop system is an architecture direction, not a completed deployment;
- current evidence should be read as sandbox-level simulation signal and diagnostic infrastructure.

## Why This Matters

Soft touch is a small task, but it is a useful stress test for embodied generalization. A model that only learns to trigger contact can exploit reward shortcuts. A model that learns contact quality needs structured observation, physical latent state, safety constraints, and transferable action representations.

That is the reason this repository is organized around the evidence loop first, then the full token control loop roadmap.
