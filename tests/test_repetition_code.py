import unittest

import numpy as np

from qsi_lab.repetition_code import (
    decode_syndrome,
    estimate_logical_error_rate,
    logical_failure,
    measure_syndrome,
    sample_bit_flip_errors,
)


class RepetitionCodeTests(unittest.TestCase):
    def test_syndrome_for_known_error_patterns(self):
        np.testing.assert_array_equal(measure_syndrome([0, 0, 0]), [0, 0])
        np.testing.assert_array_equal(measure_syndrome([0, 1, 0]), [1, 1])
        np.testing.assert_array_equal(measure_syndrome([1, 1, 0]), [0, 1])

    def test_decoder_corrects_every_pattern_with_at_most_one_error_at_distance_three(self):
        for errors in ([0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]):
            with self.subTest(errors=errors):
                correction = decode_syndrome(measure_syndrome(errors))
                self.assertFalse(logical_failure(errors, correction))

    def test_decoder_detects_uncorrectable_two_bit_pattern(self):
        errors = [1, 1, 0]
        correction = decode_syndrome(measure_syndrome(errors))
        self.assertTrue(logical_failure(errors, correction))

    def test_sampling_is_reproducible_with_seeded_generator(self):
        first = sample_bit_flip_errors(np.random.default_rng(12), 5, 0.2)
        second = sample_bit_flip_errors(np.random.default_rng(12), 5, 0.2)
        np.testing.assert_array_equal(first, second)

    def test_zero_physical_error_has_no_logical_failures(self):
        result = estimate_logical_error_rate(3, 0.0, 100, np.random.default_rng(1))
        self.assertEqual(result, (0, 0.0, 0.0))

    def test_rejects_even_distance(self):
        with self.assertRaises(ValueError):
            decode_syndrome([0, 0, 0])


if __name__ == "__main__":
    unittest.main()
