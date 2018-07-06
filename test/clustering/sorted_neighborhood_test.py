# =============================================================================
# Fog Sorted Neighborhood Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from Levenshtein import distance as levenshtein
from fog.clustering import sorted_neighborhood

DATA = [
    'Abelard',
    'Abelar',
    'Atrium',
    'Atrides',
    'Belgian',
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
