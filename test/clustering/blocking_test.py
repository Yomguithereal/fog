# =============================================================================
# Fog Blocking Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from Levenshtein import distance as levenshtein
from fog.clustering import blocking
from fog.tokenizers import ngrams

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


class TestBlocking(object):
    def test_basics(self):

        # Blocking on first letter
        clusters = Clusters(blocking(DATA, blocks=lambda x: x[0], distance=levenshtein, radius=1))

        assert clusters == CLUSTERS
