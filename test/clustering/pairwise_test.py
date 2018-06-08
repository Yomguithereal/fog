# =============================================================================
# Fog Pairwise Clustering Unit Tests
# =============================================================================
from Levenshtein import distance as levenshtein
from fog.clustering import (
    pairwise_leader,
    pairwise_fuzzy_clusters,
    pairwise_connected_components
)

DATA = [
    'abc',
    'bcd',
    'cde',
    'def',
    'efg',
    'fgh',
    'ghi'
]

LEADER_CLUSTERS = [
    ['abc', 'bcd'],
    ['cde', 'def'],
    ['efg', 'fgh']
]

FUZZY_CLUSTERS = [
    ['abc', 'bcd'],
    ['cde', 'bcd', 'def'],
    ['efg', 'def', 'fgh'],
    ['ghi', 'fgh']
]

MIN_FUZZY_CLUSTERS = [
    ['bcd', 'abc', 'cde'],
    ['def', 'cde', 'efg'],
    ['fgh', 'efg', 'ghi']
]


class TestPairwiseClustering(object):
    def test_pairwise_leader(self):
        clusters = list(pairwise_leader(DATA, distance=levenshtein, radius=2))

        assert clusters == LEADER_CLUSTERS

    def test_pairwise_fuzzy_clusters(self):
        clusters = list(pairwise_fuzzy_clusters(DATA, distance=levenshtein, radius=2))

        assert clusters == FUZZY_CLUSTERS

        min_clusters = list(pairwise_fuzzy_clusters(DATA, distance=levenshtein, radius=2, min_size=3))

        assert min_clusters == MIN_FUZZY_CLUSTERS

        parallel_clusters = list(pairwise_fuzzy_clusters(DATA, distance=levenshtein, radius=2, processes=2, chunk_size=3))

        assert parallel_clusters == FUZZY_CLUSTERS

    def test_pairwise_connected_components(self):
        clusters = list(pairwise_connected_components(DATA, distance=levenshtein, radius=2))

        assert clusters == [DATA]
