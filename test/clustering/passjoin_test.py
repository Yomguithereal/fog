# =============================================================================
# Fog PassJoin Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from fog.clustering import passjoin
from fog.clustering.passjoin import (
    multi_match_aware_interval,
    multi_match_aware_substrings,
    partition,
    segments
)


EXPECTED_INTERVALS = [
    ((1, 0, 0), (0, 0)),
    ((1, 1, 2), (1, 3)),
    ((1, 2, 4), (4, 6)),
    ((1, 3, 6), (7, 7))
]

MULTI_MATCH_AWARE_TESTS = [
    (
        (0, 7, ['a']),
        (1, 7, ['at']),
        (2, 7, ['re']),
        (3, 7, ['ha'])
    ),

    (
        (0, 8, ['av']),
        (1, 8, ['at', 'ta']),
        (2, 8, ['re', 'es']),
        (3, 8, ['ha'])
    ),

    (
        (0, 9, ['av']),
        (1, 9, ['va', 'at', 'ta']),
        (2, 9, ['ar', 're', 'es']),
        (3, 9, ['sha'])
    ),

    (
        (0, 10, ['av']),
        (1, 10, ['va', 'at', 'ta']),
        (2, 10, ['tar', 'are', 'res']),
        (3, 10, ['sha'])
    ),

    (
        (0, 11, ['av']),
        (1, 11, ['vat', 'ata', 'tar']),
        (2, 11, ['tar', 'are', 'res']),
        (3, 11, ['sha'])
    ),

    (
        (0, 12, ['ava']),
        (1, 12, ['ata', 'tar']),
        (2, 12, ['are', 'res']),
        (3, 12, ['sha'])
    ),

    (
        (0, 13, ['ava']),
        (1, 13, ['ata']),
        (2, 13, ['are']),
        (3, 13, ['esha'])
    )
]

STRINGS = [
    'benjamin',
    'paule',
    'paul',
    'pa',
    'benja',
    'benjomon',
    'ab',
    'a',
    ''
]

CLUSTERS_K1 = Clusters([
    ['paul', 'paule'],
    ['', 'a', 'pa', 'ab']
])

CLUSTERS_K2 = Clusters([
    ['benjamin', 'benjomon'],
    ['', 'a', 'ab', 'pa', 'paul', 'paule']
])

CLUSTERS_K3 = Clusters([
    ['benjamin', 'benjomon', 'benja'],
    ['', 'a', 'ab', 'pa', 'paul', 'paule']
])


class TestPassJoins(object):
    def test_segments(self):
        assert list(segments(3, 'vankatesh')) == [(0, 'va'), (1, 'nk'), (2, 'at'), (3, 'esh')]
        assert list(segments(3, 'avaterasha')) == [(0, 'av'), (1, 'at'), (2, 'era'), (3, 'sha')]

    def test_multi_match_aware_interval(self):
        for (delta, i, pi), interval in EXPECTED_INTERVALS:
            assert multi_match_aware_interval(3, delta, i, pi) == interval

    def test_multi_match_aware_substrings(self):
        for group in MULTI_MATCH_AWARE_TESTS:
            for (i, l, substrings), (_, pi, li) in zip(group, partition(3, group[0][1])):
                assert list(multi_match_aware_substrings(3, 'avaterasha', l, i, pi, li))

        # Duplicate letters
        substrings = list(multi_match_aware_substrings(3, 'avatssssha', 11, 2, 5, 3))

        # NOTE: should not duplicate 'sss'
        assert substrings == ['tss', 'sss']

    def test_passjoin(self):

        # k = 1
        clusters = Clusters(passjoin(STRINGS, 1))

        assert clusters == CLUSTERS_K1

        clusters = Clusters(passjoin(STRINGS, 1, sort=False))

        assert clusters == CLUSTERS_K1

        # k = 2
        clusters = Clusters(passjoin(STRINGS, 2))

        assert clusters == CLUSTERS_K2

        clusters = Clusters(passjoin(STRINGS, 2, sort=False))

        assert clusters == CLUSTERS_K2

        # k = 3
        clusters = Clusters(passjoin(STRINGS, 3))

        assert clusters == CLUSTERS_K3

        clusters = Clusters(passjoin(STRINGS, 3, sort=False))

        assert clusters == CLUSTERS_K3
