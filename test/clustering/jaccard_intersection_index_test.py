# =============================================================================
# Fog Jaccard Intersection Index Clustering Unit Tests
# =============================================================================
from test.clustering.utils import Clusters
from fog.clustering import jaccard_intersection_index

DATA = [
    'abcde',
    'abcdeg',
    'zyx'
]

CLUSTERS = Clusters([
    ('abcde', 'abcdeg')
])


class TestJaccardIntersectionIndex(object):
    def test_basics(self):
        clusters = Clusters(jaccard_intersection_index(DATA, radius=0.8))

        assert clusters == CLUSTERS
