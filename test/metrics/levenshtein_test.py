# =============================================================================
# Fog Levenshtein Distance Unit Tests
# =============================================================================
import math
from pytest import approx
from fog.metrics import (
    levenshtein_distance,
    limited_levenshtein_distance,
    levenshtein_distance_lte1,
    damerau_levenshtein_distance_lte1
)

BASIC_TESTS = [
    # (('b', 'o', 'o', 'k'), ('b', 'a', 'c', 'k'), 2),
    # (('the', 'cat', 'eats', 'mouse'), ('the', 'mouse', 'likes', 'mouse'), 2),
    ('book', 'back', 2),
    ('bbbbookkkk', 'bbbbackkkk', 2),
    ('hello', 'helo', 1),
    ('good sir', 'baal', 8),
    ('say', 'shiver', 5),
    ('feature', 'get-project-features', 13),
    ('example', 'samples', 3),
    ('sturgeon', 'urgently', 6),
    ('levenshtein', 'frankenstein', 6),
    ('distance', 'difference', 5),
    ('a', 'b', 1),
    ('ab', 'ac', 1),
    ('ac', 'bc', 1),
    ('abc', 'axc', 1),
    ('xabxcdxxefxgx', '1ab2cd34ef5g6', 6),
    ('a', '', 1),
    ('ab', 'a', 1),
    ('ab', 'b', 1),
    ('abc', 'ac', 1),
    ('xabxcdxxefxgx', 'abcdefg', 6),
    ('', 'a', 1),
    ('a', 'ab', 1),
    ('b', 'ab', 1),
    ('ac', 'abc', 1),
    ('abcdefg', 'xabxcdxxefxgx', 6),
    ('', '', 0),
    ('a', 'a', 0),
    ('abc', 'abc', 0),
    ('', '', 0),
    ('a', '', 1),
    ('', 'a', 1),
    ('abc', '', 3),
    ('', 'abc', 3),
    ('因為我是中國人所以我會說中文', '因為我是英國人所以我會說英文', 2),
    # (list('因為我是中國人所以我會說中文'), list('因為我是英國人所以我會說英文'), 2)
]

HELLO_WORDS = [
    'BONJOUR',
    'BINJOUR',
    'BONTOUR',
    'NONJOUR',
    'ONJOUR',
    'BONJOU',
    'BONJOURE',
    'BONTJOUR',
    'TBONJOUR'
]

HELLO_WORDS_TRANSPOSITIONS = [
    'OBNJOUR',
    'BNOJOUR',
    'BOJNOUR',
    'BONOJUR',
    'BONJORU'
]

LEVENSHTEIN_LTE1_TESTS = [
    ('BONJOUR', 'BONJOURE', True),
    ('TBONJOUR', 'BONJOUR', True),
    ('BONTOUR', 'BONJOUR', True),
    ('BONJOUR', 'MONJOUR', True),
    ('BONJOUR', 'BONJOUT', True),
    ('BMNJOURE', 'BONJOUR', False),
    ('MONJOURE', 'BONJOUR', False),
    ('BTONJOUR', 'BONJOUR', True),
    ('BONJOUR', 'F', False),
    ('BONJOUR', 'BNOJOURE', False),
    ('BONJOUR', 'BONJOURES', False),
    ('Faylan', 'Fayray', False),
    ('Loane', 'Loona', False),
    ('David Byrne', 'David Byron', False),
    ('Willie Nix', 'Willie Nile', False),
    ('DJ Spinna', 'DJ Spinbad', False),
    ('Lian Ross', 'Diana Ross', False),
    ('Diana', 'Lian', False)
]


class TestLevenshteinSimilarity(object):
    def test_basics(self):
        for A, B, distance in BASIC_TESTS:
            assert levenshtein_distance(A, B) == distance, '%s // %s => %i' % (A, B, distance)

    def test_limited(self):
        for A, B, distance in BASIC_TESTS:
            assert limited_levenshtein_distance(2, A, B) == (distance if distance <= 2 else 3)

    def test_lte1(self):
        for A, B, distance in BASIC_TESTS:
            assert levenshtein_distance_lte1(A, B) == (distance <= 1)

        for word in HELLO_WORDS:
            assert levenshtein_distance_lte1(word, 'BONJOUR')
            assert levenshtein_distance_lte1('BONJOUR', word)

        for A, B, result in LEVENSHTEIN_LTE1_TESTS:
            assert levenshtein_distance_lte1(A, B) == result

    def test_damerau_lte1(self):
        for word in HELLO_WORDS + HELLO_WORDS_TRANSPOSITIONS:
            assert damerau_levenshtein_distance_lte1('BONJOUR', word)
            assert damerau_levenshtein_distance_lte1(word, 'BONJOUR')

        for A, B, result in LEVENSHTEIN_LTE1_TESTS:
            assert damerau_levenshtein_distance_lte1(A, B) == result

        assert not damerau_levenshtein_distance_lte1('BONJOUR', 'OTHER')
