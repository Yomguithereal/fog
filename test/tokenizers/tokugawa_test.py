# =============================================================================
# Fog Tokugawa Tokenizer Unit Tests
# =============================================================================
from fog.tokenizers.tokugawa import TokugawaTokenizer

TESTS = [
    {
        'text': 'Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\nThanks.',
        'tokens': ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York', '.', 'Please', 'buy', 'me', 'two', 'of', 'them', '.', 'Thanks', '.']
    },
    {
        'text': 'They\'ll save and invest more.',
        'tokens': ['They', '\'ll', 'save', 'and', 'invest', 'more', '.']
    },
    {
        'text': 'hi, my name can\'t hello,',
        'tokens': ['hi', ',', 'my', 'name', 'can', '\'t', 'hello', ',']
    },
    {
        'text': '"Hello", Good sir (this is appaling)...',
        'tokens': ['"', 'Hello', '"', ',', 'Good', 'sir', '(', 'this', 'is', 'appaling', ')', '.', '.', '.']
    },
    {
        'text': 'L\'amour de l’amour naît pendant l\'été!',
        'tokens': ['L\'', 'amour', 'de', 'l’', 'amour', 'naît', 'pendant', 'l\'', 'été', '!'],
        'lang': 'fr'
    },
    {
        'text': 'It all started during the 90\'s!',
        'tokens': ['It', 'all', 'started', 'during', 'the', '90', '\'s', '!']
    },
    {
        'text': 'This is some it\'s sentence. This is incredible "ok" (very) $2,4 2.4 Aujourd\'hui This, is very cruel',
        'tokens': ['This', 'is', 'some', 'it', '\'s', 'sentence', '.', 'This', 'is', 'incredible', '"', 'ok', '"', '(', 'very', ')', '$', '2,4', '2.4', 'Aujourd', '\'hui', 'This', ',', 'is', 'very', 'cruel']
    },
    {
        'text': 'This is a very nice cat 🐱! No? Family: 👨‍👨‍👧‍👧!',
        'tokens': ['This', 'is', 'a', 'very', 'nice', 'cat', '🐱', '!', 'No', '?', 'Family', ':', '👨‍👨‍👧‍👧', '!']
    }
]


class TestTokugawaTokenizer(object):
    def test_basics(self):
        for test in TESTS:
            tokenizer = TokugawaTokenizer(lang=test.get('lang', 'en'))
            # print()
            # print(test['text'])
            # print(list(tokenizer(test['text'])))
            # print()
            assert list(tokenizer(test['text'])) == test['tokens']
