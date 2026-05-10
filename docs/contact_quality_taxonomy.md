# Contact Quality Taxonomy

## Why Contact Quality Needs Its Own Metrics

Raw contact is easy to obtain in simulation. A policy can collide with the object, skim the surface, or oscillate near a threshold and still show a high touch rate. For soft-touch research, that signal is too weak.

The project therefore separates contact into stricter categories:

| Category | Meaning | Typical Risk |
| --- | --- | --- |
| `no_contact` | No meaningful contact event | task not reached |
| `raw_contact_only` | Contact occurs but fails validity checks | reward shortcut |
| `hard_contact` | Contact force or speed is too high | unsafe collision |
| `valid_unstable_touch` | Valid touch occurs but cannot be held | flicker or early release |
| `stable_soft_touch` | Low-force valid contact is held over time | desired target |
| `hover_or_signal_mismatch` | Near-surface behavior without valid physical evidence | metric mismatch |

## Core Metrics

- `touch_rate`: loose contact frequency. Useful for debugging, insufficient for claims.
- `valid_touch_rate`: share of episodes meeting strict validity conditions.
- `stable_soft_touch_rate`: share of episodes that sustain valid low-force contact.
- `over_force_rate`: share of episodes crossing force limits.
- `raw_to_valid_conversion_rate`: how often raw contact becomes valid contact.
- `first_contact_force`: force at first contact; high values indicate impact behavior.
- `first_contact_speed`: end-effector speed at first contact; high values indicate poor braking.
- `contact_streak`: whether contact is sustained or only a flicker.

## Failure Types

The current evidence loop tracks several failure modes:

- hard impact: the policy reaches the object through excessive speed or force;
- bump and retreat: the policy touches once, then loses contact;
- contact flicker: short alternating contact events without stable hold;
- near-zone reward hacking: the policy stays close enough to score but avoids valid touch;
- wrong-signal contact: a metric suggests contact while trace-level physical evidence disagrees;
- over-force dominance: `touch_rate` rises together with `over_force_rate`;
- insufficient boundary data: few examples exist near the raw-to-valid transition.

## Public Demo Boundary

The demo in this repository uses synthetic, redacted sample metrics. It demonstrates the evaluation logic. It does not include raw traces, internal experiment logs, model checkpoints, or private platform paths.
