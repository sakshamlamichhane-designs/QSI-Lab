# QSI-Lab

**Quantum Science Intelligence Laboratory** — reproducible simulation and stress-testing of quantum error correction.

## Project objective

Build a reliable, reproducible QEC workflow in stages: implement a repetition code from first principles, reproduce an established surface-code benchmark with Stim and PyMatching, validate statistical uncertainty, and only then investigate a carefully scoped question informed by the literature. Baselines and smoke tests are learning artifacts, not novelty claims.

## Today's starting work

- `src/qsi_lab/repetition_code.py`: independent bit-flip repetition-code simulator, syndrome extraction, minimum-weight decoder, and logical-failure estimate.
- `tests/test_repetition_code.py`: deterministic tests for syndromes, decoding, validation, and correction of all single-bit errors for distance 3.
- `scripts/first_surface_code.py`: standard Stim/PyMatching software smoke test (not a novel result).
- `scripts/repetition_code_experiment.py`: reproducible logical-error-rate sweep; saves a CSV and plot under `results/`.

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

If PowerShell blocks activation, run this for the current terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Run

From the repository root with the virtual environment active:

```powershell
python -m unittest discover -s tests -v
python scripts/repetition_code_experiment.py
python scripts/first_surface_code.py
```

The surface-code script uses 10,000 shots per distance at physical error probability 0.005. Its reported standard error is a binomial approximation; zero observed failures means an upper bound constrained by the sample size, not a zero true error rate.

## Reproducibility notes

- Python package dependencies are listed in `requirements.txt`.
- The repetition-code experiment uses a fixed random seed and records parameters in the CSV.
- The Stim/PyMatching smoke test intentionally follows the standard circuit-level workflow and is not evidence of a new decoder or research result.
- Keep code, parameters, outputs, environment details, interpretation, and failures together when recording experiments.

## Results log

| Date (UTC) | Experiment | Status / result |
|---|---|---|
| 2026-10-12 | Initial setup | In progress; record test and experiment outcomes after running locally. |
