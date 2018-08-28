# =============================================================================
# Fog Levenshtein 1D Key Unit Tests
# =============================================================================
from fog.key import levenshtein_1d_keys, damerau_levenshtein_1d_keys

HELLO_KEYS = set([
    'hello',
    '!ello',
    'h!llo',
    'he!lo',
    'hel!o',
    'hell!',
    '!hello',
    'h!ello',
    'he!llo',
    'hell!o',
    'hello!'
])

HELLO_TRANSPOSITION_KEYS = set([
    'ehllo',
    'hlelo',
    'helol'
])


def prettify(s):
    return s.replace('\x00', '!')


class TestLevenshtein1DKey(object):
    def test_basics(self):

        keys = set(prettify(k) for k in levenshtein_1d_keys('hello'))

        assert keys == HELLO_KEYS

        keys_with_transpositions = set(prettify(k) for k in levenshtein_1d_keys('hello', transpositions=True))

        assert keys_with_transpositions == HELLO_KEYS | HELLO_TRANSPOSITION_KEYS

        keys_with_transpositions = set(prettify(k) for k in damerau_levenshtein_1d_keys('hello'))

        assert keys_with_transpositions == HELLO_KEYS | HELLO_TRANSPOSITION_KEYS
