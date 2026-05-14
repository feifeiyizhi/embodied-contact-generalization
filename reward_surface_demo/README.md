# Reward Surface Demo

This folder contains a small public reward-surface implementation for the soft-touch simulation task.

It is included to show the engineering logic behind reward shaping:

- distance shaping near the target surface;
- preferred low-force contact around a calibrated soft-touch band;
- penalties for hard impact and high approach speed;
- a small stability bonus for sustained valid contact;
- action-smoothness regularization.

The script is intentionally self-contained. It does not train a policy, run MuJoCo, load private traces, read checkpoints, or reproduce internal experiment logs.

## Run

From the repository root:

```bash
python3 -m pip install -r reward_surface_demo/requirements.txt
python3 reward_surface_demo/reward_surface_public.py --output figures/reward_surface_public_demo.png
```

The generated figure is a public visualization of the reward shape. It should be read as reward-design evidence rather than policy-success evidence.
