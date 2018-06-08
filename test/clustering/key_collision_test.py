# =============================================================================
# Fog Key Collision Clustering Unit Tests
# =============================================================================
from Levenshtein import distance as levenshtein
from fog.clustering import key_collision
from fog.tokenizers import ngrams

DATA = [
    'Hello',
    'hello',
    'heLLo',
    'gooDbye',
    'Goodbye'
]

CLUSTERS = [
    ['Hello', 'hello', 'heLLo'],
    ['gooDbye', 'Goodbye']
]

NAMES = [
    'John Doe',
    'John Doe Jr.',
    'Mary S.',
    'Mary Silva',
    'John D.'
]

NAMES_CLUSTERS = [
    ['John Doe', 'John Doe Jr.', 'John D.'],
    ['John Doe', 'John Doe Jr.', 'John D.'],
    ['John Doe', 'John Doe Jr.'],
    ['John Doe', 'John Doe Jr.'],
    ['Mary S.', 'Mary Silva'],
    ['Mary S.', 'Mary Silva']
]

MERGED_NAMES_CLUSTERS = set([
    ('John D.', 'John Doe', 'John Doe Jr.'),
    ('Mary S.', 'Mary Silva')
])


class TestKeyCollisionClustering(object):
    def test_single_key(self):
        clusters = list(key_collision(DATA, key=lambda x: x.lower()))

        assert clusters == clusters

    def test_multiple_key(self):
        clusters = list(key_collision(NAMES, keys=lambda x: ngrams(5, x)))

        assert clusters == NAMES_CLUSTERS

    def test_multiple_keys_merged(self):
        clusters = list(key_collision(NAMES, keys=lambda x: ngrams(5, x), merge=True))
        clusters = set(tuple(sorted(c)) for c in clusters)

        assert clusters == MERGED_NAMES_CLUSTERS
