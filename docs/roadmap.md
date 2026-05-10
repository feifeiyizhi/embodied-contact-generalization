# Roadmap

## Stage 1: Evidence Loop

Build a contact-quality evaluation loop that can distinguish raw contact, hard contact, valid touch, unstable touch, and stable soft touch.

Deliverables:

- strict metric definitions;
- failure taxonomy;
- fixed evaluation reports;
- redacted public demo;
- data availability boundaries.

Current repository status: included.

## Stage 2: Boundary Data And Diagnostics

Collect or synthesize more examples around the raw-to-valid boundary. The purpose is to make the transition between unsafe, invalid, and stable contact learnable.

Deliverables:

- episode-level contact labels;
- trace-level summaries;
- small public examples;
- private full-trace review pipeline.

Current repository status: design described; private traces withheld.

## Stage 3: DreamerV3 World Model

Train a compact world model from contact-rich rollouts. Use RSSM latent states to represent contact history, force onset, sensor noise, and approach dynamics.

Deliverables:

- latent dynamics training script;
- reconstruction and prediction diagnostics;
- imagined rollout checks;
- failure-conditioned latent analysis.

Current repository status: roadmap direction.

## Stage 4: Token Action Prediction

Condition action-token prediction on observation tokens, goal/context tokens, and `z(t)` latent tokens from the world model.

Deliverables:

- action token schema;
- next-action-token predictor;
- safety wrapper;
- offline replay evaluation;
- simulator-in-the-loop validation.

Current repository status: architecture direction.

## Stage 5: Task Transfer

Test whether the same representation transfers beyond soft touch, for example to gentle insertion, rack alignment, fragile-object placement, or labware handling.

Deliverables:

- multiple contact-sensitive task suites;
- shared metric schema;
- task-conditioned rollout analysis;
- transfer evaluation.

Current repository status: future work.
