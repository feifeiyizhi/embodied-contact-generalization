# Architecture Direction

## From Specialized Control Chains To Unified Representation

Many robot-control systems are assembled as a specialized chain:

```text
perception -> state estimation -> policy -> action mapping / MPC -> motor execution
```

This structure is effective for well-scoped tasks, yet each layer often carries task-specific assumptions. The research direction here is a unified control representation where perception, latent dynamics, task context, and action generation are expressed as tokens inside one control loop.

## Full Token Control Loop

The target loop is:

```text
sensor / observation tokens
+ latent state z(t) tokens
+ goal / context tokens
        |
        v
DreamerV3 world model engine
        |
        v
RSSM latent dynamics and imagined rollouts
        |
        v
Emu3.5 token action predictor
        |
        v
safety wrapper / low-level motor execution
```

The goal is task-general embodied control. Soft touch is the first measurable task because it tests whether the system can learn contact quality instead of merely producing contact.

## Three Layers

### 1. Emu3.5 Meta-Optimizer

At the high level, Emu3.5-style multimodal modeling can read task context, diagnostic summaries, visual states, and prior rollout evidence. Its role is to propose or select task-conditioned strategies, evaluation focus, and parameter regions.

This layer is a research direction. It should not be read as current direct motor control.

### 2. DreamerV3 World Model Engine

DreamerV3 provides the world-model component. A recurrent state-space model learns a compact latent state `z(t)` from observation history and predicts future representations. Imagined rollouts can reduce the cost of checking every mechanism with real simulator episodes.

For the soft-touch setting, the important signal is contact dynamics: force onset, wrist-sensor history, approach speed, valid-touch windows, instability, and over-force risk. A world model can still learn these structures from reconstruction and latent prediction losses when reward gates are noisy or sparse.

An ACE-style asymmetric actor-critic variant is also compatible with this route: the critic may use simulator-side privileged force information during training, while the actor remains constrained to realistic sensor history. This is listed as a roadmap option, not a completed public result.

### 3. Emu3.5 Token Control Loop

At the low level, action generation is formulated as next-action-token prediction:

```text
[observation tokens, z(t), goal/context tokens] -> [action tokens]
```

The critical design point is direct conditioning on the RSSM latent state `z(t)`. Action prediction should depend on a learned physical state, not just on raw current observations or a hand-written controller state. This couples physical regularity learning with action generation inside one loop.

## Safety Wrapper

Even in a tokenized control loop, motor execution requires safety checks:

- force and velocity thresholds;
- over-force termination;
- action clipping;
- contact-state sanity checks;
- fallback or stop behavior when uncertainty is high.

The safety wrapper is part of the architecture, not an afterthought. For contact-sensitive tasks, safe execution defines which action tokens are admissible.

## Current Boundary

The repository describes an architecture direction and a diagnostic evidence loop. It does not claim that the complete DreamerV3 + Emu3.5 closed-loop controller has been implemented or validated.
