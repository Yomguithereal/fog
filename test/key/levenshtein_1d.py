# =============================================================================
# Fog Levenshtein 1D Key Unit Tests
# =============================================================================
from fog.key import (
    levenshtein_1d_keys,
    damerau_levenshtein_1d_keys,
    damerau_levenshtein_1d_blocks
)

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

HELLO_WORDS = [
    'BONJOUR',
    'BINJOUR',
    'BONTOUR',
    'NONJOUR',
    'ONJOUR',
    'BONJOU',
    'BONJOURE',
    'BONTJOUR',
    'TBONJOUR',
    'BOJNOUR',
    'BONOJUR',
    'OBNJOUR'
]


def prettify(s):
    return s.replace('\x00', '!')


class TestLevenshtein1D(object):
    def test_keys(self):

        keys = set(prettify(k) for k in levenshtein_1d_keys('hello'))

        assert keys == HELLO_KEYS

        keys_with_transpositions = set(prettify(k) for k in levenshtein_1d_keys('hello', transpositions=True))

        assert keys_with_transpositions == HELLO_KEYS | HELLO_TRANSPOSITION_KEYS

        keys_with_transpositions = set(prettify(k) for k in damerau_levenshtein_1d_keys('hello'))

        assert keys_with_transpositions == HELLO_KEYS | HELLO_TRANSPOSITION_KEYS

    def test_blocks(self):

        assert damerau_levenshtein_1d_blocks('T') == ('T', )
        assert damerau_levenshtein_1d_blocks('BONBON') == ('BON', )

        hello_blocks = damerau_levenshtein_1d_blocks('BONJOUR')

        for word in HELLO_WORDS:
            blocks = damerau_levenshtein_1d_blocks(word)

            assert any(b in hello_blocks for b in blocks)
