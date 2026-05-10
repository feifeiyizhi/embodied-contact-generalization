# Soft-Touch Evidence Report

Dataset note: Synthetic redacted sample for public evidence-loop demonstration.

## Aggregate Metrics

- episodes: 6
- touch_rate: 66.7%
- valid_touch_rate: 33.3%
- stable_soft_touch_rate: 16.7%
- over_force_rate: 16.7%
- raw_to_valid_conversion_rate: 50.0%
- over_force_among_touched: 25.0%
- first_contact_force_mean: 11.575
- first_contact_force_p90: 24.260
- first_contact_speed_mean: 0.295
- first_contact_speed_p90: 0.570

## Episode Labels

- no_contact: 1
- hover_or_signal_mismatch: 1
- raw_contact_only: 1
- hard_contact: 1
- valid_unstable_touch: 1
- stable_soft_touch: 1

## Interpretation

The sample contains stable soft-touch examples, but aggregate quality still depends on repeatability and force tails.

This report is diagnostic. It does not claim policy success, real-robot readiness, or completion of the full token control loop.

## Per-Episode Classification

| episode_id | label | raw_contact | valid_touch | stable_soft_touch | over_force |
| --- | --- | --- | --- | --- | --- |
| sample_001 | hard_contact | True | False | False | True |
| sample_002 | valid_unstable_touch | True | True | False | False |
| sample_003 | stable_soft_touch | True | True | True | False |
| sample_004 | no_contact | False | False | False | False |
| sample_005 | hover_or_signal_mismatch | False | False | False | False |
| sample_006 | raw_contact_only | True | False | False | False |
