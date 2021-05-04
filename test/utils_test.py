# =============================================================================
# Fog Generic Utils Unit Tests
# =============================================================================
from pytest import approx, raises
from statistics import mean, StatisticsError

from fog.utils import squeeze, OnlineMean

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

    def test_online_mean(self):
        values = [1, 4, 3, 1, 6, 7, -16, 46, 4.5, 1, 4, 3, 6.18, 72, 0, 0]

        online_mean = OnlineMean()

        with raises(StatisticsError):
            online_mean.peek()

        for x in values:
            online_mean.add(x)

        assert online_mean.peek() == approx(mean(values))
        assert len(online_mean) == len(values)

        for x in values[:5]:
            online_mean.subtract(x)

        assert online_mean.peek() == approx(mean(values[5:]))
        assert len(online_mean) == len(values[5:])

        with raises(TypeError):
            online_mean += 45

        online_mean = OnlineMean()

        for x in values[:5]:
            online_mean.add(x)

        remaining = OnlineMean()

        for x in values[5:]:
            remaining.add(x)

        total = online_mean + remaining

        assert isinstance(total, OnlineMean)
        assert total is not online_mean and total is not remaining

        assert total.peek() == approx(mean(values))

        online_mean += remaining

        assert online_mean.peek() == approx(mean(values))
