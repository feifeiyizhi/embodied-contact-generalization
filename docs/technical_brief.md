# Technical Brief: Embodied Contact Generalization

This project studies task-general embodied control through a minimum soft-touch task. The public repository is a compact research-engineering showcase: it exposes the problem definition, representative MuJoCo model, reward-surface logic, diagnostic metrics, and a small evidence-loop demo. It excludes raw traces, checkpoints, internal audit notes, private dashboards, and full experiment reports.

## Current State

- Current claim tier: `sandbox_signal`.
- PPO allowed: `false`.
- Training / GPU / public RJob status for the latest public update: none.
- Current platform: simplified MuJoCo 3-DOF soft-touch research platform.
- Current result boundary: approximate soft-touch candidates and diagnostic wrappers have appeared in simulation, but no official soft-touch success is claimed.
- Latest engineering status: private CPU-only diagnostics produced a narrow force-tail safety-wrapper candidate and retained the raw mapper as the reference baseline. The next stage is boundary-gate redesign plus leakage-free world-model diagnostics.

The strongest current value is not a finished controller. The value is the evidence loop: separating loose contact from valid touch, stable soft touch, hard impact, early release, and gate mismatch.

## Platform Spec

The public reference XML is [models/arm3dof_touch.xml](../models/arm3dof_touch.xml).

| Item | Public spec |
| --- | --- |
| Simulator | MuJoCo |
| Robot | simplified 3-DOF arm, not a full real robot and not a dexterous hand |
| Joints | `joint1`, `joint2`, `joint3`; all hinge joints around z-axis |
| Actuators | `m1`, `m2`, `m3`; one motor per joint |
| State dimensions | `qpos[:3]`, `qvel[:3]` |
| Action | 3D normalized action in `[-1, 1]` |
| Action execution | action smoothing / scaling -> joint target delta -> PD torque -> MuJoCo motor control |
| Default sim dt | `0.002 s` |
| Default control dt | `0.05 s` |
| Substeps | `round(ctrl_dt / sim_dt) = 25` MuJoCo steps per control step |
| Default action scale | `0.20 rad` target-joint delta scale |
| Default PD | `kp=200`, `kd=20`, torque limit `30` |
| End effector | `ee_geom`, sphere radius `0.025 m` |
| Target | `target_geom`, cylinder radius `0.04 m`, half-height `0.005 m`, nominal height `0.50 m` |
| Touch radius | `0.045 m`, used as task/contact-quality scale rather than a real sensor radius |
| Contact material | default friction `0.8 0.02 0.001`, `condim=6`, `solimp=0.99 0.999 0.001` |
| Force band | valid force from `0.10 N` to strict upper limit, with gentle limit `4.0 N` |
| Hold gate | low speed, stable action, stable force, and small surface-gap variation for multiple steps |

### Signals

Deployable-facing signals:

- joint position and velocity: `qpos`, `qvel`;
- previous action and executed action;
- wrist force / torque analog from the MuJoCo `ft_force` and `ft_torque` site sensors, assuming real hardware has comparable sensing.

MuJoCo-only diagnostic signals:

- exact geom-pair contact between `ee_geom` and `target_geom`;
- simulator contact wrench from `mj_contactForce`;
- exact surface gap, penetration, body pose, and hidden solver state;
- post-hoc labels such as `valid_touch`, `stable_soft_touch`, `over_force`, and terminal reason.

Actor-facing models must not depend on MuJoCo-only diagnostic labels at decision time. Those labels are useful for evaluation, teacher-target construction, and failure taxonomy.

## Contact Quality Definitions

- `raw_target_contact`: the end-effector and target geoms touch in MuJoCo.
- `target_contact_gate`: raw contact plus geometric gate consistency, including z/gap constraints.
- `valid_touch`: contact is within force, speed, surface, and stability gates for the required hold window.
- `stable_soft_touch`: valid touch sustained long enough under the gentle-force and stable-hold gates.
- `over_force`: contact force exceeds the strict force bound.
- `raw_contact_only`: contact occurs, but it fails the valid-touch gates.

This distinction matters because a controller can increase `touch_rate` while still producing hard contact or unstable grazing. Public figures therefore emphasize `valid_touch_rate`, `stable_soft_touch_rate`, `over_force_rate`, first-contact force, and first-contact speed.

## Why World Models Fit This Environment

DreamerV3 is relevant because the task is partially observable, contact-rich, and sensitive to short-horizon dynamics. Its world-model route can learn latent transition structure from replay data, use imagined rollouts for candidate screening, and normalize force/return scales before a controller is widened.

The proposed control loop is:

```text
sensor / observation tokens
+ state or RSSM latent z(t) tokens
+ goal / context tokens
        |
        v
DreamerV3-style world model for contact dynamics
        |
        v
z(t)-conditioned next-action-token prediction
        |
        v
safety wrapper and motor execution
```

The key design point is that the RSSM latent state `z(t)` should directly condition action-token prediction. That links learned physical dynamics and action generation inside one closed loop instead of treating the world model as a detached analysis module.

## How Prior Data Helps

Existing simulation artifacts are useful as replay and diagnostic data:

- Transition/event data provides failure labels, action/state context, and contact-quality transitions.
- Wrapper diagnostics identify where simple action mapping improves or fails.
- Reward-surface probes expose which force, distance, speed, and smoothness terms create useful gradients.
- Boundary cases are especially valuable because they show where a candidate does not extrapolate.

These data should be reused as an offline diagnostic corpus before any new training. Re-ingesting old failure data from scratch is unnecessary.

## Pitfalls

- Leakage: future labels, branch IDs, scenario IDs, and MuJoCo-only contact truth must not become actor inputs.
- Unit mismatch: meters, radians, Newtons, torque units, control-step deltas, and MuJoCo substep quantities must be kept separate.
- Contact aliasing: a `0.05 s` control step contains 25 physics substeps, so first-contact force can peak inside one control step.
- PD mismatch: the policy action is not motor torque; it becomes a joint target delta, then PD torque, then clipped motor control.
- Contact stiffness: `solimp`, friction, damping, armature, timestep, and torque limits can make the platform behave like a heavy tool when the target behavior is fine soft touch.
- Model bias: a world model can screen candidates, but MuJoCo rollout remains the truth source until calibration gates pass.

## Next Route

1. Keep the raw mapper as the reference baseline.
2. Redesign the boundary gate around transition-boundary force tails and action-diff attribution.
3. Build a leakage-free DreamerV3-style diagnostic world model from existing replay data.
4. Use `z(t)` only as a candidate-conditioning signal after clean validation; do not treat world-model prediction as truth.
5. Keep the safety wrapper in the execution path for force, velocity, action-delta, and stop conditions.

## References

- Hafner et al., DreamerV3, "Mastering Diverse Domains through World Models": https://arxiv.org/abs/2301.04104
- DreamerV3 reference implementation: https://github.com/danijar/dreamerv3
- MuJoCo XML reference: https://mujoco.readthedocs.io/en/stable/XMLreference.html
