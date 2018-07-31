# =============================================================================
# Fog Sorted Neighborhood Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from Levenshtein import distance as levenshtein
from fog.clustering import sorted_neighborhood, adaptive_sorted_neighborhood

DATA = [
    'Belgian',
    'Abelard',
    'Atrium',
    'Atrides',
    'Abelar',
    'Belgia',
    'Telgia'
]

CLUSTERS = Clusters([
    ('Abelard', 'Abelar'),
    ('Belgian', 'Belgia')
])


class TestSortedNeighborhood(object):
    def test_basics(self):

        # Sorting alphabetically
        clusters = Clusters(sorted_neighborhood(DATA, distance=levenshtein, radius=1, window=2))

        assert clusters == CLUSTERS

    def test_adaptive(self):

        # Sorting alphabetically
        clusters = Clusters(adaptive_sorted_neighborhood(DATA, distance=levenshtein, radius=1, window=2))

        assert clusters == CLUSTERS
