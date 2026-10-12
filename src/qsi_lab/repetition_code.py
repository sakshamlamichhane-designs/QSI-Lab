"""Bit-flip repetition-code simulator and minimum-weight decoder."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.random import Generator


def _validate_distance(distance: int) -> None:
    if isinstance(distance, bool) or not isinstance(distance, int) or distance < 1:
        raise ValueError("distance must be a positive integer")
    if distance % 2 == 0:
        raise ValueError("distance must be odd for an unambiguous majority decoder")


def _validate_bits(bits: Sequence[int], expected_length: int, name: str) -> np.ndarray:
    values = np.asarray(bits)
    if values.ndim != 1 or len(values) != expected_length:
        raise ValueError(f"{name} must be a one-dimensional sequence of length {expected_length}")
    if not np.all(np.isin(values, (0, 1))):
        raise ValueError(f"{name} must contain only 0 and 1")
    return values.astype(np.uint8, copy=False)


def sample_bit_flip_errors(rng: Generator, distance: int, physical_error_rate: float) -> np.ndarray:
    """Draw independent bit-flip errors for one codeword."""
    _validate_distance(distance)
    if not 0 <= physical_error_rate <= 1:
        raise ValueError("physical_error_rate must be between 0 and 1")
    return rng.binomial(1, physical_error_rate, size=distance).astype(np.uint8)


def measure_syndrome(errors: Sequence[int]) -> np.ndarray:
    """Return adjacent parity checks s_i = e_i XOR e_(i+1)."""
    error_bits = np.asarray(errors)
    if error_bits.ndim != 1 or len(error_bits) < 1 or not np.all(np.isin(error_bits, (0, 1))):
        raise ValueError("errors must be a non-empty one-dimensional binary sequence")
    return np.bitwise_xor(error_bits[:-1], error_bits[1:]).astype(np.uint8)


def decode_syndrome(syndrome: Sequence[int]) -> np.ndarray:
    """Infer the minimum-weight error consistent with a repetition-code syndrome.

    The two candidates differ by an all-qubit logical bit flip. For odd code
    distance, their weights cannot tie, so choosing the lower-weight candidate
    is equivalent to majority-vote decoding.
    """
    syndrome_bits = np.asarray(syndrome)
    if syndrome_bits.ndim != 1 or not np.all(np.isin(syndrome_bits, (0, 1))):
        raise ValueError("syndrome must be a one-dimensional binary sequence")
    distance = len(syndrome_bits) + 1
    _validate_distance(distance)

    candidates = []
    for first_bit in (0, 1):
        candidate = np.empty(distance, dtype=np.uint8)
        candidate[0] = first_bit
        for index, check in enumerate(syndrome_bits):
            candidate[index + 1] = candidate[index] ^ check
        candidates.append(candidate)
    return min(candidates, key=lambda candidate: int(candidate.sum())).copy()


def logical_failure(errors: Sequence[int], correction: Sequence[int]) -> bool:
    """Return whether applying correction leaves the logical bit flipped."""
    error_bits = np.asarray(errors)
    if error_bits.ndim != 1 or len(error_bits) < 1:
        raise ValueError("errors must be a non-empty one-dimensional sequence")
    error_bits = _validate_bits(error_bits, len(error_bits), "errors")
    correction_bits = _validate_bits(correction, len(error_bits), "correction")
    residual = np.bitwise_xor(error_bits, correction_bits)
    return bool(np.all(residual == 1))


def estimate_logical_error_rate(
    distance: int,
    physical_error_rate: float,
    shots: int,
    rng: Generator,
) -> tuple[int, float, float]:
    """Estimate logical failures; return (failures, rate, binomial standard error)."""
    _validate_distance(distance)
    if not 0 <= physical_error_rate <= 1:
        raise ValueError("physical_error_rate must be between 0 and 1")
    if isinstance(shots, bool) or not isinstance(shots, int) or shots <= 0:
        raise ValueError("shots must be a positive integer")

    failures = 0
    for _ in range(shots):
        errors = sample_bit_flip_errors(rng, distance, physical_error_rate)
        correction = decode_syndrome(measure_syndrome(errors))
        failures += logical_failure(errors, correction)
    rate = failures / shots
    standard_error = float(np.sqrt(rate * (1 - rate) / shots))
    return failures, rate, standard_error
