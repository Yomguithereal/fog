# =============================================================================
# Fog Ngrams Unit Tests
# =============================================================================
import math
from fog.tokenizers import ngrams, bigrams, trigrams, quadrigrams
from fog.tokenizers.ngrams import join_ngrams

ALIASES = [None, bigrams, trigrams, quadrigrams]

STRING = 'Bonjour'

STRING_TESTS = [
    ('B', 'o', 'n', 'j', 'o', 'u', 'r'),
    ('Bo', 'on', 'nj', 'jo', 'ou', 'ur'),
    ('Bon', 'onj', 'njo', 'jou', 'our'),
    ('Bonj', 'onjo', 'njou', 'jour')
]

SENTENCE = tuple('the cat eats the mouse'.split(' '))

SENTENCE_TEST = [
    (('the',), ('cat',), ('eats',), ('the',), ('mouse',)),
    (('the', 'cat'), ('cat', 'eats'), ('eats', 'the'), ('the', 'mouse')),
    (('the', 'cat', 'eats'), ('cat', 'eats', 'the'), ('eats', 'the', 'mouse')),
    (('the', 'cat', 'eats', 'the'), ('cat', 'eats', 'the', 'mouse'))
]


class TestNgrams(object):
    def test_basics(self):
        for i in range(4):
            assert tuple(ngrams(i + 1, STRING)) == STRING_TESTS[i]
            assert tuple(ngrams(i + 1, SENTENCE)) == SENTENCE_TEST[i]

            alias = ALIASES[i]

            if alias is not None:
                assert tuple(alias(STRING)) == STRING_TESTS[i]
                assert tuple(alias(SENTENCE)) == SENTENCE_TEST[i]

    def test_join(self):
        for i in range(4):
            assert join_ngrams(ngrams(i + 1, STRING)) == STRING

    def test_too_short(self):
        assert list(ngrams(5, 'yop')) == ['yop']
