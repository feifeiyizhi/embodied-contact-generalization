# Qingmiao Support Note

This repository supports a Qingmiao-style review by showing the project as a hands-on research build rather than a polished success claim.

The project starts from a concrete physical bottleneck: contact quality. In simulation, a controller can often reach an object while still failing the real requirement of gentle, stable, low-force touch. This makes soft touch a useful minimum task for embodied generalization. It exposes whether the system learns contact dynamics, safety constraints, and state history, or only learns a shortcut to trigger loose contact.

The current public materials show three kinds of work:

- problem formulation: converting a vague embodied-control goal into measurable contact-quality criteria;
- engineering discipline: separating loose contact, valid touch, stable soft touch, over-force, and trace-level mismatch;
- architecture direction: moving from specialized control chains toward a full token control loop with DreamerV3 latent dynamics and Emu3.5-style action-token prediction.

The main technical hypothesis is that the DreamerV3 RSSM latent state `z(t)` should directly condition action-token prediction. This connects learned physical dynamics with action generation in the same loop. The current repository presents this as a roadmap and design direction; it does not present a completed closed-loop deployment.

For Qingmiao review, the important signal is the builder pattern:

- define a difficult physical behavior precisely;
- build a small evaluation loop before making large claims;
- keep failure categories inspectable;
- withhold raw private artifacts while preserving a runnable public example;
- use evidence from the minimum task to guide a broader embodied-model architecture.

The repository should be read as research-in-progress with sandbox-level diagnostic evidence.
