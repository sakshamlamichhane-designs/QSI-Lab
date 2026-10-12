"""Run a seeded repetition-code logical-error-rate sweep and save its artifacts."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from qsi_lab.repetition_code import estimate_logical_error_rate


SEED = 20261012
SHOTS = 20_000
DISTANCES = (3, 5, 7)
PHYSICAL_ERROR_RATES = (0.01, 0.03, 0.05, 0.07, 0.10, 0.15)
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    rng = np.random.default_rng(SEED)
    rows = []
    for distance in DISTANCES:
        for physical_rate in PHYSICAL_ERROR_RATES:
            failures, logical_rate, standard_error = estimate_logical_error_rate(
                distance, physical_rate, SHOTS, rng
            )
            rows.append(
                {
                    "distance": distance,
                    "physical_error_rate": physical_rate,
                    "shots": SHOTS,
                    "failures": failures,
                    "logical_error_rate": logical_rate,
                    "standard_error": standard_error,
                    "seed": SEED,
                }
            )
            print(
                f"d={distance}, p={physical_rate:.3f}: "
                f"failures={failures}/{SHOTS}, logical_rate={logical_rate:.6g}, "
                f"approx_SE={standard_error:.2g}"
            )

    csv_path = RESULTS_DIR / "repetition_code_sweep.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    figure, axis = plt.subplots(figsize=(7, 5))
    for distance in DISTANCES:
        selected = [row for row in rows if row["distance"] == distance]
        axis.errorbar(
            [row["physical_error_rate"] for row in selected],
            [row["logical_error_rate"] for row in selected],
            yerr=[row["standard_error"] for row in selected],
            marker="o",
            capsize=3,
            label=f"distance {distance}",
        )
    axis.plot(PHYSICAL_ERROR_RATES, PHYSICAL_ERROR_RATES, "k--", alpha=0.5, label="p_L = p")
    axis.set(xlabel="Physical bit-flip probability p", ylabel="Logical failure probability per shot")
    axis.set_title(f"Bit-flip repetition code ({SHOTS:,} shots per point)")
    axis.grid(True, alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(RESULTS_DIR / "repetition_code_sweep.png", dpi=160)
    plt.close(figure)
    print(f"Saved {csv_path} and {RESULTS_DIR / 'repetition_code_sweep.png'}")


if __name__ == "__main__":
    main()
