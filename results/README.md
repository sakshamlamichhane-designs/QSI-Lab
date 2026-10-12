# First experiment log

## Repetition-code sweep

- Run date: 2026-10-12
- Script: `scripts/repetition_code_experiment.py`
- Model: independent bit-flip errors, perfect syndrome measurement, minimum-weight/majority decoder
- Distances: 3, 5, 7
- Physical error probabilities: 0.01, 0.03, 0.05, 0.07, 0.10, 0.15
- Shots per point: 20,000
- Seed: 20261012
- Outputs: `repetition_code_sweep.csv`, `repetition_code_sweep.png`

### Interpretation

For these sampled points, the logical failure rate generally decreases as odd repetition-code distance increases at fixed physical error probability. This is the expected behavior for the repetition code under independent bit flips and perfect syndrome measurements below its threshold of 1/2. This is a basic validation/learning result, not a novel research claim. The repetition code protects against one Pauli error type only and is not a full quantum code.

At distance 5 and physical error probability 0.01, no failures occurred in 20,000 shots. The observed rate is zero, but the true logical error rate is not thereby shown to be zero; the reported plug-in binomial standard error is also zero in that special case and should not be mistaken for a useful confidence bound. Increasing shots or using a confidence interval is needed to quantify rare-event rates.

## Surface-code pipeline smoke test

- Run date: 2026-10-12
- Script: `scripts/first_surface_code.py`
- Circuit: Stim `surface_code:rotated_memory_x`, rounds equal to distance
- Noise probability: 0.005 for each configured circuit-level channel
- Shots per distance: 10,000
- Decoder: PyMatching built from Stim detector error model
- Purpose: verify that simulation and decoding run together; not a novel result.

Observed output:

| Distance | Failures | Observed logical error rate | Approx. standard error |
|---:|---:|---:|---:|
| 3 | 196 / 10,000 | 0.0196 | 0.0014 |
| 5 | 183 / 10,000 | 0.0183 | 0.0013 |
| 7 | 130 / 10,000 | 0.0130 | 0.0011 |

The sampled logical error rate trends downward with distance here. This is only a modest-shot software smoke test, not a validated reproduction of a reference figure. The full experiment specification, package versions, circuit choices, and uncertainty treatment must be compared with the chosen reference before describing it as a reproduced benchmark.

## Validation

- Unit tests: 6 passed.
- Package import check: NumPy, Matplotlib, pandas, Stim, and PyMatching imported successfully.
- Failures/blockers: none encountered in this initial run.
