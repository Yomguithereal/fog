# =============================================================================
# Fog Pairwise Clustering Unit Tests
# =============================================================================
from test.clustering.utils import Clusters
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

LEADER_CLUSTERS = Clusters([
    ['abc', 'bcd'],
    ['cde', 'def'],
    ['efg', 'fgh']
])

FUZZY_CLUSTERS = Clusters([
    ['abc', 'bcd'],
    ['cde', 'bcd', 'def'],
    ['efg', 'def', 'fgh'],
    ['ghi', 'fgh']
])

MIN_FUZZY_CLUSTERS = Clusters([
    ['bcd', 'abc', 'cde'],
    ['def', 'cde', 'efg'],
    ['fgh', 'efg', 'ghi']
])


class TestPairwiseClustering(object):
    def test_pairwise_leader(self):
        clusters = Clusters(pairwise_leader(DATA, distance=levenshtein, radius=2))

        assert clusters == LEADER_CLUSTERS

    def test_pairwise_fuzzy_clusters(self):
        clusters = Clusters(pairwise_fuzzy_clusters(DATA, distance=levenshtein, radius=2))

        assert clusters == FUZZY_CLUSTERS

        min_clusters = Clusters(pairwise_fuzzy_clusters(DATA, distance=levenshtein, radius=2, min_size=3))

        assert min_clusters == MIN_FUZZY_CLUSTERS

        parallel_clusters = Clusters(pairwise_fuzzy_clusters(DATA, distance=levenshtein, radius=2, processes=2, chunk_size=3))

        assert parallel_clusters == FUZZY_CLUSTERS

        # Using custom keys
        keyed_data = [(1.0, d) for d in DATA]

        clusters = Clusters([i[1] for i in c] for c in pairwise_fuzzy_clusters(keyed_data, distance=levenshtein, radius=2, key=lambda x: x[1]))

        assert clusters == FUZZY_CLUSTERS

    def test_pairwise_connected_components(self):
        clusters = Clusters(pairwise_connected_components(DATA, distance=levenshtein, radius=2))

        assert clusters == Clusters([DATA])

        # Using custom keys
        keyed_data = [(1.0, d) for d in DATA]

        clusters = Clusters(pairwise_connected_components(keyed_data, distance=levenshtein, radius=2, key=lambda x: x[1]))

        assert clusters == Clusters([keyed_data])
