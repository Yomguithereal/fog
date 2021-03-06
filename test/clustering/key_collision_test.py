# =============================================================================
# Fog Key Collision Clustering Unit Tests
# =============================================================================
from test.clustering.utils import Clusters
from fog.clustering import key_collision
from fog.tokenizers import ngrams

DATA = [
    'Hello',
    'hello',
    'heLLo',
    'gooDbye',
    'Goodbye'
]

CLUSTERS = Clusters([
    ['Hello', 'hello', 'heLLo'],
    ['gooDbye', 'Goodbye']
])

FALSEY_CLUSTERS = Clusters([
    ['hello', 'heLLo'],
    ['gooDbye', 'Goodbye']
])

NAMES = [
    'John Doe',
    'John Doe Jr.',
    'Mary S.',
    'Mary Silva',
    'John D.'
]

NAMES_CLUSTERS = Clusters([
    ['John Doe', 'John Doe Jr.', 'John D.'],
    ['John Doe', 'John Doe Jr.', 'John D.'],
    ['John Doe', 'John Doe Jr.'],
    ['John Doe', 'John Doe Jr.'],
    ['Mary S.', 'Mary Silva'],
    ['Mary S.', 'Mary Silva']
])

MERGED_NAMES_CLUSTERS = Clusters([
    ['John D.', 'John Doe', 'John Doe Jr.'],
    ['Mary S.', 'Mary Silva']
])


class TestKeyCollisionClustering(object):
    def test_single_key(self):
        clusters = Clusters(key_collision(DATA, key=lambda x: x.lower()))

        assert clusters == CLUSTERS

    def test_multiple_key(self):
        clusters = Clusters(key_collision(NAMES, keys=lambda x: ngrams(5, x), merge=False))

        assert clusters == NAMES_CLUSTERS

    def test_multiple_keys_merged(self):
        clusters = Clusters(key_collision(NAMES, keys=lambda x: ngrams(5, x)))

        assert clusters == MERGED_NAMES_CLUSTERS

    def test_falsey_keys(self):
        clusters = Clusters(key_collision(DATA, key=lambda x: x.lower() if x != 'Hello' else None))

        assert clusters == FALSEY_CLUSTERS

        clusters = Clusters(key_collision(DATA, keys=lambda x: [x.lower()] if x != 'Hello' else None))

        assert clusters == FALSEY_CLUSTERS
