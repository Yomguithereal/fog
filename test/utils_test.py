# =============================================================================
# Fog Generic Utils Unit Tests
# =============================================================================
from fog.utils import squeeze

SQUEEZE_TESTS = [
    ('Ellement', 'Element'),
    ('ggggrrrrr', 'gr'),
    ('GGgrr', 'Ggr'),
    ('King Setis XXII', 'King Setis XI')
]


class TestUtils(object):
    def test_squeeze(self):
        for string, result in SQUEEZE_TESTS:
            assert squeeze(string) == result

        assert squeeze('King Setis XXII', keep_roman_numerals=True) == 'King Setis XXII'
