"""Standard Stim/PyMatching surface-code pipeline smoke test, not a novel result."""

import numpy as np
import pymatching
import stim


SHOTS = 10_000
PHYSICAL_ERROR_RATE = 0.005


def main() -> None:
    for distance in (3, 5, 7):
        circuit = stim.Circuit.generated(
            "surface_code:rotated_memory_x",
            distance=distance,
            rounds=distance,
            after_clifford_depolarization=PHYSICAL_ERROR_RATE,
            before_round_data_depolarization=PHYSICAL_ERROR_RATE,
            after_reset_flip_probability=PHYSICAL_ERROR_RATE,
            before_measure_flip_probability=PHYSICAL_ERROR_RATE,
        )
        detector_model = circuit.detector_error_model(decompose_errors=True)
        decoder = pymatching.Matching.from_detector_error_model(detector_model)
        sampler = circuit.compile_detector_sampler()
        syndrome, actual_observables = sampler.sample(
            shots=SHOTS,
            separate_observables=True,
        )
        predicted_observables = decoder.decode_batch(syndrome)
        failures = int(np.any(predicted_observables != actual_observables, axis=1).sum())
        rate = failures / SHOTS
        standard_error = np.sqrt(rate * (1 - rate) / SHOTS)
        print(
            f"d={distance}: failures={failures}/{SHOTS}, "
            f"logical_error_rate={rate:.6g}, approx_SE={standard_error:.2g}"
        )


if __name__ == "__main__":
    main()
