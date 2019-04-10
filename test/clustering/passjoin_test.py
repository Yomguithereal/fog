# =============================================================================
# Fog PassJoin Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from fog.clustering.passjoin import multi_match_aware_interval


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
