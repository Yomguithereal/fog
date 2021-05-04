# =============================================================================
# Fog Dice Coefficient Unit Tests
# =============================================================================
from fog.metrics import dice_coefficient
from fog.tokenizers import bigrams

TESTS = [
    ('healed', 'healed', 1),
    ('healed', 'sealed', 0.8),
    ('healed', 'healthy', 6 / 11),
    ('healed', 'heard', 4 / 9),
    ('healed', 'herded', 0.4),
    ('healed', 'help', 0.25),
    ('healed', 'sold', 0),
    ('tomato', 'tomato', 1),
    ('h', 'help', 0),
    ('h', 'h', 1),
    ('', '', 1),
    ('h', 'g', 0)
]


class TestDiceCoefficient(object):
    def test_basics(self):
        for A, B, coefficient in TESTS:
            A = set(bigrams(A))
            B = set(bigrams(B))

            assert dice_coefficient(A, B) == coefficient
