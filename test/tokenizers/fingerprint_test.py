# =============================================================================
# Fog Fingerprint Tokenizer Unit Tests
# =============================================================================
from fog.tokenizers import (
    FingerprintTokenizer,
    fingerprint_tokenizer,
    ngrams_fingerprint_tokenizer
)

from fog.key import (
    fingerprint,
    ngrams_fingerprint
)

TESTS = [
    ('', ''),
    ('hello', 'hello'),
    ('Tom Cruise', 'cruise tom'),
    ('The mouse is a mouse', 'a is mouse the'),
    ('électricité', 'electricite'),
    ('\x00Hello', 'hello'),
    ('Hello?', 'hello'),
    ('« très bien ! »', 'bien tres')
]

NGRAMS_TESTS = [
    (2, '', ''),
    (2, 'Paris', 'arispari'),
    (1, 'Paris', 'aiprs'),
    (2, 'bébé', 'beeb'),
    (3, 'PariS', 'ariparris')
]


class TestFingerprintTokenizer(object):
    def test_basics(self):

        for string, key in TESTS:
            assert ' '.join(fingerprint_tokenizer(string)) == key
            assert fingerprint(string) == key

    def test_stopwords(self):
        tokenizer = FingerprintTokenizer(stopwords=['de'])

        assert tokenizer('Université de Paris') == ['paris', 'universite']

    def test_digits(self):
        tokenizer = FingerprintTokenizer(keep_digits=False)

        assert tokenizer('20 grammes de maïß') == ['de', 'grammes', 'maiss']

    def test_min_token_size(self):
        tokenizer = FingerprintTokenizer(min_token_size=2)

        assert tokenizer('a very good cat') == ['cat', 'good', 'very']

    def test_split(self):
        tokenizer = FingerprintTokenizer(min_token_size=2, split=[',', '-'])

        assert tokenizer('l\'université de Bade-Wurt') == ['bade', 'universite', 'wurt']

    def test_squeeze(self):
        tokenizer = FingerprintTokenizer(squeeze=True)

        assert tokenizer('Russian Barnett') == ['barnet', 'rusian']

    def test_ngrams(self):

        for n, string, key in NGRAMS_TESTS:
            assert ''.join(ngrams_fingerprint_tokenizer(n, string)) == key
            assert ngrams_fingerprint(n, string) == key
