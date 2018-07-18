# =============================================================================
# Fog Overlap Coefficient Unit Tests
# =============================================================================
from pytest import approx
from fog.metrics import overlap_coefficient

TESTS = [
    ('abc', 'abc', 1.0),
    ('abc', 'def', 0.0),
    ('abc', 'abd', 2 / 3),
    ('abc', 'abcde', 1),
    ('abcdefij', 'abc', 1),
    (list('abcdefij'), list('abc'), 1),
    ((1, 2, 3), (1, 2), 1),
    ('aaaaaaabc', 'aaabbbbbbc', 1.0)
]


class TestOverlapCoefficient(object):
    def test_basics(self):
        for A, B, coefficient in TESTS:
            assert overlap_coefficient(A, B) == coefficient
