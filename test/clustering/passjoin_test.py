# =============================================================================
# Fog PassJoin Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from fog.clustering.passjoin import multi_match_aware_interval, segments


EXPECTED_INTERVALS = [
    ((1, 0, 0), (0, 0)),
    ((1, 1, 2), (1, 3)),
    ((1, 2, 4), (4, 6)),
    ((1, 3, 6), (7, 7))
]


class TestPassJoins(object):
    def test_multi_match_aware_interval(self):
        for (delta, i, pi), interval in EXPECTED_INTERVALS:
            assert multi_match_aware_interval(3, delta, i, pi) == interval

    def test_segments(self):
        assert list(segments(3, 'vankatesh')) == [(0, 'va'), (1, 'nk'), (2, 'at'), (3, 'esh')]
        assert list(segments(3, 'avaterasha')) == [(0, 'av'), (1, 'at'), (2, 'era'), (3, 'sha')]
