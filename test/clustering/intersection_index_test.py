# =============================================================================
# Fog Intersection Index Clustering Unit Tests
# =============================================================================
from test.clustering.utils import Clusters
from fog.clustering import intersection_index

DATA = [
    'abcde',
    'abcdeg',
    'abcdegfjexge',
    'zyx'
]

CLUSTERS = Clusters([
    ('abcde', 'abcdeg')
])

OVERLAP_CLUSTERS = Clusters([
    ('abcde', 'abcdeg', 'abcdegfjexge')
])


class TestIntersectionIndex(object):
    def test_basics(self):
        clusters = Clusters(intersection_index(DATA, radius=0.8))

        assert clusters == CLUSTERS

    def test_overlap(self):
        clusters = Clusters(intersection_index(DATA, radius=0.8, metric='overlap'))

        assert clusters == OVERLAP_CLUSTERS
