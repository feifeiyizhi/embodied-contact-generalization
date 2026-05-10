# Project Overview

## Research Question

The project asks how an embodied model can acquire task-general contact skills rather than a single task-specific control trick. The immediate validation target is soft touch: a robot should make contact with an object gently, maintain it stably, and avoid hard collision or reward shortcuts.

Soft touch is used as a minimum validation task because it compresses several hard problems into one measurable setting:

- contact dynamics are discontinuous and sensitive to force, velocity, friction, and sensor timing;
- loose contact is easy to fake, while stable low-force contact is much harder;
- reward signals can be exploited unless strict metrics and failure labels are maintained;
- the same contact-quality representation can later transfer to lab automation, precision assembly, and fragile-object manipulation.

## Current Work

The current implementation work has focused on building a reliable simulation evidence loop:

- strict contact-quality metrics such as `valid_touch_rate`, `stable_soft_touch_rate`, `over_force_rate`, first-contact force, and first-contact speed;
- failure taxonomy for hard contact, raw-contact-only behavior, surface hovering, contact flicker, early release, and reward hacking;
- fixed evaluation and trace review habits that separate operational execution from scientific evidence;
- redacted public examples that show how soft-touch evidence is interpreted without exposing internal logs or checkpoints.

This work is valuable even before a final policy exists. It turns a vague embodied-control goal into observable failure modes and repeatable evaluation criteria.

## Architecture Direction

The next technical route is a full token control loop:

```text
sensor tokens + latent state z(t) tokens + goal/context tokens
    -> world-model learning and imagined rollouts
    -> next-action-token prediction
    -> safety wrapper / motor execution
```

DreamerV3-style latent dynamics are used as the world-model engine. Emu3.5-style multimodal modeling is used in two roles: high-level meta-optimization over task context, and low-level action-token prediction in the control loop.

The core hypothesis is that `z(t)` from a recurrent state-space model should directly condition action-token prediction. This gives the action generator access to a compact representation of contact dynamics, including force and contact history, instead of depending only on immediate observations or manually shaped state variables.

## Status

The project is currently at the evidence-loop and architecture-design stage. It has not reached a public claim of solved soft-touch control, real-robot deployment, or completed DreamerV3 + Emu3.5 closed-loop execution. The current value lies in the metric system, failure analysis, redacted diagnostic demo, and the roadmap toward unified embodied representations.

## Qingmiao Fit

This project reflects a builder-oriented research style: define a hard physical problem, make it measurable, expose failure modes, and use the resulting evidence to decide the next mechanism. The GitHub materials are therefore organized as a research showcase with a runnable diagnostic demo rather than a polished product repository.
