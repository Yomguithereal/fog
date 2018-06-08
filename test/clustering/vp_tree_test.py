# =============================================================================
# Fog VPTree Clustering Unit Tests
# =============================================================================
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

FUZZY_CLUSTERS = set([
    ('abc', 'bcd'),
    ('bcd', 'cde', 'def'),
    ('def', 'efg', 'fgh'),
    ('fgh', 'ghi')
])

MIN_FUZZY_CLUSTERS = set([
    ('abc', 'bcd', 'cde'),
    ('cde', 'def', 'efg'),
    ('efg', 'fgh', 'ghi')
])


class TestVPTreeClustering(object):
    def test_basics(self):
        clusters = list(vp_tree(DATA, distance=levenshtein, radius=2))
        clusters = set(tuple(sorted(c)) for c in clusters)

        assert clusters == FUZZY_CLUSTERS

        clusters = list(vp_tree(DATA, distance=levenshtein, radius=2, min_size=3))
        clusters = set(tuple(sorted(c)) for c in clusters)
