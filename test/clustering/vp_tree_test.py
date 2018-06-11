# =============================================================================
# Fog VPTree Clustering Unit Tests
# =============================================================================
from test.clustering.utils import Clusters
from Levenshtein import distance as levenshtein
from fog.clustering import vp_tree

DATA = [
    'abc',
    'bcd',
    'cde',
    'def',
    'efg',
    'fgh',
    'ghi'
]

FUZZY_CLUSTERS = Clusters([
    ('abc', 'bcd'),
    ('bcd', 'cde', 'def'),
    ('def', 'efg', 'fgh'),
    ('fgh', 'ghi')
])

MIN_FUZZY_CLUSTERS = Clusters([
    ('abc', 'bcd', 'cde'),
    ('cde', 'def', 'efg'),
    ('efg', 'fgh', 'ghi')
])


class TestVPTreeClustering(object):
    def test_basics(self):
        clusters = Clusters(vp_tree(DATA, distance=levenshtein, radius=2))

        assert clusters == FUZZY_CLUSTERS

        clusters = Clusters(vp_tree(DATA, distance=levenshtein, radius=2, min_size=3))

        assert clusters == MIN_FUZZY_CLUSTERS
