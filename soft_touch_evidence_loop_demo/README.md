# Soft-Touch Evidence Loop Demo

This demo reads redacted sample episode metrics and writes a Markdown evidence report.

It is a diagnostic example, not a controller and not a training script.

## Run

```bash
python3 run_demo.py sample_metrics.json demo_report.md
```

## What It Shows

The script separates:

- loose contact from valid contact;
- valid but unstable contact from stable soft touch;
- hard contact from safe low-force contact;
- aggregate operational signals from claim-worthy contact-quality evidence.

