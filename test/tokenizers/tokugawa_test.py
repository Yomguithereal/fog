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
        'tokens': ['hi', ',', 'my', 'name', 'can\'t', 'hello', ',']
    },
    {
        'text': '"Hello", Good sir (this is appaling)...',
        'tokens': ['"', 'Hello', '"', ',', 'Good', 'sir', '(', 'this', 'is', 'appaling', ')', '.', '.', '.']
    },
    {
        'text': 'L\'amour de l’amour naît pendant l\'été!',
        'tokens': ['L\'', 'amour', 'de', 'l’', 'amour', 'naît', 'pendant', 'l\'', 'été', '!']
    },
    {
        'text': 'It all started during the 90\'s!',
        'tokens': ['It', 'all', 'started', 'during', 'the', '90', '\'s', '!']
    },
    {
        'text': 'This is some it\'s sentence. This is incredible "ok" (very) $2,4 2.4 Aujourd\'hui This, is very cruel',
        'tokens': ['This', 'is', 'some', 'it', '\'s', 'sentence', '.', 'This', 'is', 'incredible', '"', 'ok', '"', '(', 'very', ')', '$', '2,4', '2.4', 'Aujourd\'hui', 'This', ',', 'is', 'very', 'cruel']
    },
    {
        'text': 'This is a very nice cat 🐱! No? Family: 👨‍👨‍👧‍👧!',
        'tokens': ['This', 'is', 'a', 'very', 'nice', 'cat', '🐱', '!', 'No', '?', 'Family', ':', '👨‍👨‍👧‍👧', '!']
    },
    {
        'text': 'Control:\x01\t\t\n ok? Wo\x10rd',
        'tokens': ['Control', ':', 'ok', '?', 'Wo', 'rd']
    },
    {
        'text': '',
        'tokens': []
    },
    {
        'text': 'hello world',
        'tokens': ['hello', 'world']
    },
    {
        'text': 'O.N.U. La vie.est foutue',
        'tokens': ['O.N.U.', 'La', 'vie', '.', 'est', 'foutue']
    },
    {
        'text': 'L\'O.N.U est dans la place',
        'tokens': ['L\'', 'O.N.U', 'est', 'dans', 'la', 'place']
    },
    {
        'text': 'Les É.U. sont nuls.',
        'tokens': ['Les', 'É.U.', 'sont', 'nuls', '.']
    },
    {
        'text': '@start/over #123 This is so #javascript @Yomguithereal! $cash',
        'tokens': ['@start', '/', 'over', '#', '123', 'This', 'is', 'so', '#javascript', '@Yomguithereal', '!', '$cash']
    },
    {
        'text': '@start/over #123 This is so #javascript @Yomguithereal! $cash',
        'tokens': ['@', 'start', '/', 'over', '#', '123', 'This', 'is', 'so', '#', 'javascript', '@', 'Yomguithereal', '!', '$', 'cash'],
        'mentions': False,
        'hashtags': False
    },
    {
        'text': 'I\'ve been. I\'ll be. You\'re mean. You\'ve lost. I\'d be. I\'m nice. It\'s a shame!',
        'tokens': ['I', "'ve", 'been', '.', 'I', "'ll", 'be', '.', 'You', "'re", 'mean', '.', 'You', "'ve", 'lost', '.', 'I', "'d", 'be', '.', 'I', "'m", 'nice', '.', 'It', "'s", 'a', 'shame', '!']
    },
    {
        'text': 'Aren\'t I?',
        'tokens': ['Aren\'t', 'I', '?']
    },
    {
        'text': '\'Tis but a jest. \'twas in vain alas! But \'tis ok!',
        'tokens': ["'Tis", 'but', 'a', 'jest', '.', "'twas", 'in', 'vain', 'alas', '!', 'But', "'tis", 'ok', '!']
    },
    {
        'text': 'D\'mitr N\'Guyen O\'Doherty O\'Hara Mbappé M\'bappé M\'Leod N\'diaye N\'Djaména L\'Arrivée m\'appeler sur l\'herbe',
        'tokens': ["D'mitr", "N'Guyen", "O'Doherty", "O'Hara", 'Mbappé', "M'bappé", "M'Leod", "N'diaye", "N'Djaména", "L'Arrivée", "m'", 'appeler', 'sur', "l'", 'herbe']
    }
]


class TestTokugawaTokenizer(object):
    def test_basics(self):
        for test in TESTS:
            tokenizer = TokugawaTokenizer(
                mentions=test.get('mentions', True),
                hashtags=test.get('hashtags', True)
            )
            # print()
            # print(test['text'])
            # print(list(tokenizer(test['text'])))
            # print()
            assert list(tokenizer(test['text'])) == test['tokens']
