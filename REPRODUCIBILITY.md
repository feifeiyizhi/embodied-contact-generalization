# Reproducibility

The public reproducibility surface is the evidence-loop demo. It requires only Python 3 and the standard library.

```bash
cd soft_touch_evidence_loop_demo
python3 run_demo.py sample_metrics.json demo_report.md
```

Expected behavior:

- reads `sample_metrics.json`;
- classifies each episode into a contact-quality label;
- computes aggregate rates and first-contact statistics;
- writes `demo_report.md`.

This demo is intentionally limited. It does not train a policy, run MuJoCo, call a model API, launch GPU jobs, or reproduce private experiments.

The purpose is to make the evaluation logic inspectable:

- loose contact is separated from valid touch;
- hard contact is separated from low-force contact;
- stable soft touch is treated as a stricter category than one-frame contact;
- aggregate metrics are interpreted under a claim-safe boundary.

Private traces, checkpoints, internal logs, and platform-specific scripts are withheld from this showcase repository.
