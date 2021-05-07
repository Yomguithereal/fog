# =============================================================================
# Fog Word Tokenizer Unit Tests
# =============================================================================
from pytest import raises

from fog.tokenizers.words import WordTokenizer, punct_emoji_iter

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
        'text': 'This is.Another',
        'tokens': ['This', 'is', '.', 'Another']
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
        'tokens': ["D'mitr", "N'Guyen", "O'Doherty", "O'Hara", 'Mbappé', "M'bappé", "M'Leod", "N'diaye", "N'Djaména", "L'", 'Arrivée', "m'", 'appeler', 'sur', "l'", 'herbe']
    },
    {
        'text': 'Those numbers 4.5, 5,6 and 2.3.4 and 2.3. and 2.5.5.3. or 4.5.stop',
        'tokens': ['Those', 'numbers', '4.5', ',', '5,6', 'and', '2.3', '.', '4', 'and', '2.3', '.', 'and', '2.5', '.', '5.3', '.', 'or', '4.5', '.', 'stop']
    },
    {
        'text': '1. Whatever, 2. something else?',
        'tokens': ['1', '.', 'Whatever', ',', '2', '.', 'something', 'else', '?']
    },
    {
        'text': 'Mr. Goldberg is dead with mlle. Jordan etc. What a day!',
        'tokens': ['Mr.', 'Goldberg', 'is', 'dead', 'with', 'mlle.', 'Jordan', 'etc.', 'What', 'a', 'day', '!']
    },
    {
        'text': 'L\'#amour appartient à l\'@ange!',
        'tokens': ['L', '#amour', 'appartient', 'à', 'l', '@ange', '!']
    },
    {
        'text': 'La température est de -23. Il est -sûr que cela va arriver.',
        'tokens': ['La', 'température', 'est', 'de', '-23', '.', 'Il', 'est', '-', 'sûr', 'que', 'cela', 'va', 'arriver', '.']
    },
    {
        'text': 'One url: https://lemonde.fr/test another one http://www.lemonde.fr/protect.html',
        'tokens': ['One', 'url', ':', 'https://lemonde.fr/test', 'another', 'one', 'http://www.lemonde.fr/protect.html']
    },
    {
        'text': 'email:john@whatever.net',
        'tokens': ['email', ':', 'john@whatever.net']
    },
    {
        'text': 'Checkout this ----> https://www.facebook.com, <--',
        'tokens': ['Checkout', 'this', '---->', 'https://www.facebook.com', ',', '<--']
    },
    {
        'text': 'Love you :). Bye <3',
        'tokens': ['Love', 'you', ':)', '.', 'Bye', '<3']
    },
    {
        'text': 'This is a cooool #dummysmiley: :-) :-P <3 and some arrows < > -> <--',
        'tokens': ['This', 'is', 'a', 'cooool', '#dummysmiley', ':', ':-)', ':-P', '<3', 'and', 'some', 'arrows', '<', '>', '->', '<--']
    },
    {
        'text': 'Such a nice kiss: :3 :\'(',
        'tokens': ['Such', 'a', 'nice', 'kiss', ':', ':3', ":'("]
    },
    {
        'text': 'This ends with #',
        'tokens': ['This', 'ends', 'with', '#']
    },
    {
        'text': 'This ends with @',
        'tokens': ['This', 'ends', 'with', '@']
    },
    {
        'text': 'This is my mother-in-law.',
        'tokens': ['This', 'is', 'my', 'mother-in-law', '.']
    },
    {
        'text': 'This is a very_cool_identifier',
        'tokens': ['This', 'is', 'a', 'very_cool_identifier']
    },
    {
        'text': 'Un véritable chef-d\'œuvre!',
        'tokens': ['Un', 'véritable', "chef-d'œuvre", '!']
    },
    {
        'text': 'This is -not cool- ok-',
        'tokens': ['This', 'is', '-', 'not', 'cool', '-', 'ok', '-']
    },
    {
        'text': '7e 1er 7eme 7ème 7th 1st 3rd 2nd 2d 11º',
        'tokens': ['7e', '1er', '7eme', '7ème', '7th', '1st', '3rd', '2nd', '2d', '11º']
    },
    {
        'text': '7even e11even l33t',
        'tokens': ['7even', 'e11even', 'l33t']
    },
    {
        'text': 'qu\'importe le flacon pourvu qu\'on ait l\'ivresse!',
        'tokens': ["qu'", 'importe', 'le', 'flacon', 'pourvu', "qu'", 'on', 'ait', "l'", 'ivresse', '!']
    },
    {
        'text': '4.5...',
        'tokens': ['4.5', '.', '.', '.']
    },
    {
        'text': 'Ça fait plaise d’être né en 98 ça fait on a connu les 2 étoiles 🙏⭐️⭐️',
        'tokens': ['Ça', 'fait', 'plaise', 'd’', 'être', 'né', 'en', '98', 'ça', 'fait', 'on', 'a', 'connu', 'les', '2', 'étoiles', '🙏', '⭐️', '⭐️']
    },
    {
        'text': 'PUTAIN CHAMPION JE VOUS AIMES PLUS QUE TOUT⚽️⚽️🤩🇫🇷#ÉpopéeRusse',
        'tokens': ['PUTAIN', 'CHAMPION', 'JE', 'VOUS', 'AIMES', 'PLUS', 'QUE', 'TOUT', '⚽️', '⚽️', '🤩', '🇫🇷', '#ÉpopéeRusse']
    },
    {
        'text': 'Ce soir je suis au calme devant ma tv, et je réalise que PUTAIN ON CHAMPIONS DU MONDE. ⭐️🇫🇷⭐️  #ÉpopéeRusse',
        'tokens': ['Ce', 'soir', 'je', 'suis', 'au', 'calme', 'devant', 'ma', 'tv', ',', 'et', 'je', 'réalise', 'que', 'PUTAIN', 'ON', 'CHAMPIONS', 'DU', 'MONDE', '.', '⭐️', '🇫🇷', '⭐️', '#ÉpopéeRusse']
    },
    {
        'text': 'Test OF.',
        'tokens': ['Test', 'OF', '.']
    },
    {
        'text': '@ThibautLe_Gal @RemyGudin @GenerationsMvt @EELV Jadot désigné tête de liste par EELV. Pas de liste commune.',
        'tokens': ['@ThibautLe_Gal', '@RemyGudin', '@GenerationsMvt', '@EELV', 'Jadot', 'désigné', 'tête', 'de', 'liste', 'par', 'EELV', '.', 'Pas', 'de', 'liste', 'commune', '.']
    },
    {
        'text': "Le Fonds pour L'Oréal et l’Industrie et l’Innovation d’Australie",
        'tokens': ['Le', 'Fonds', 'pour', "L'", 'Oréal', 'et', 'l’', 'Industrie', 'et', 'l’', 'Innovation', 'd’', 'Australie']
    },
    {
        'text': '🙏,🙏, ,🙏,,,🙏',
        'tokens': ['🙏', ',', '🙏', ',', ',', '🙏', ',', ',', ',', '🙏']
    },
    {
        'text': '.@f_i_t_s_l_h: hello',
        'tokens': ['.', '@f_i_t_s_l_h', ':', 'hello']
    },
    {
        'text': 'facturé €4 Millions',
        'tokens': ['facturé', '€', '4', 'Millions']
    },
    {
        'text': 'va-t-on est-il 15-20-minute talk peut-on dis-moi dis-le dis-lui vas-y dit-elle',
        'tokens': ['va', 't', 'on', 'est', 'il', '15-20-minute', 'talk', 'peut', 'on', 'dis', 'moi', 'dis', 'le', 'dis', 'lui', 'vas', 'y', 'dit', 'elle']
    },
    {
        'text': 'This is VERY 2.5 🙏 importANT!',
        'lower': True,
        'tokens': ['this', 'is', 'very', '2.5', '🙏', 'important', '!']
    },
    {
        'text': 'élémentaire non?',
        'unidecode': True,
        'tokens': ['elementaire', 'non', '?']
    },
    {
        'text': 'A mouse eats the cheese.',
        'min_word_length': 4,
        'tokens': ['mouse', 'eats', 'cheese', '.']
    },
    {
        'text': 'A mouse eats the cheese 🙏.',
        'stoplist': ['a', 'the', '🙏'],
        'tokens': ['A', 'mouse', 'eats', 'cheese', '.']
    },
    {
        'text': 'A mouse eats the cheese 🙏.',
        'stoplist': ['a', 'THE', '🙏'],
        'lower': True,
        'tokens': ['mouse', 'eats', 'cheese', '.']
    },
    {
        'text': 'A mouse eats the 3.4 cheese 🙏.',
        'keep': ['emoji', 'punct'],
        'tokens': ['🙏', '.']
    },
    {
        'text': 'A mouse eats the 3.4 cheese 🙏.',
        'drop': ['emoji', 'punct', 'number'],
        'tokens': ['A', 'mouse', 'eats', 'the', 'cheese']
    },
    {
        'text': 'Loooool I know riiiiiight? Cool.',
        'reduce_words': True,
        'tokens': ['Loool', 'I', 'know', 'riiight', '?', 'Cool', '.']
    }
]


class TestWordTokenizer(object):
    def test_exceptions(self):
        with raises(TypeError, match='unknown'):
            WordTokenizer(keep=['test'])

        with raises(TypeError, match='unknown'):
            WordTokenizer(drop=['test'])

        with raises(TypeError, match='both'):
            WordTokenizer(keep=['word'], drop=['emoji'])

    def test_punct_emoji_iter(self):
        results = list(punct_emoji_iter('🙏,🙏,'))
        assert results == [('emoji', '🙏'), ('punct', ','), ('emoji', '🙏'), ('punct', ',')]

        results = list(punct_emoji_iter(',🙏,,,🙏,'))
        assert results == [('punct', ','), ('emoji', '🙏'), ('punct', ','), ('punct', ','), ('punct', ','), ('emoji', '🙏'), ('punct', ',')]

        results = list(punct_emoji_iter('⭐️.🙏⭐️⭐️,⭐️'))
        assert results == [('emoji', '⭐️'), ('punct', '.'), ('emoji', '🙏'), ('emoji', '⭐️'), ('emoji', '⭐️'), ('punct', ','), ('emoji', '⭐️')]

    def test_basics(self):
        for test in TESTS:
            tokenizer = WordTokenizer(
                lower=test.get('lower', False),
                unidecode=test.get('unidecode', False),
                reduce_words=test.get('reduce_words', False),
                min_word_length=test.get('min_word_length'),
                stoplist=test.get('stoplist'),
                keep=test.get('keep'),
                drop=test.get('drop')
            )

            # print()
            # print(test['text'])
            # print(list(token for _, token in tokenizer(test['text'])))

            assert list(token for _, token in tokenizer(test['text'])) == test['tokens']

    def test_token_types(self):
        tokenizer = WordTokenizer()

        tokens = list(tokenizer('This 1st 2.9 2,5, -34, :-) https://www.lemonde.fr - 🙏⭐️⭐️ yomgui@github.net 🐱 #test @yomgui # @'))

        assert tokens == [
            ('word', 'This'),
            ('word', '1st'),
            ('number', '2.9'),
            ('number', '2,5'),
            ('punct', ','),
            ('number', '-34'),
            ('punct', ','),
            ('smiley', ':-)'),
            ('url', 'https://www.lemonde.fr'),
            ('punct', '-'),
            ('emoji', '🙏'),
            ('emoji', '⭐️'),
            ('emoji', '⭐️'),
            ('email', 'yomgui@github.net'),
            ('emoji', '🐱'),
            ('hashtag', '#test'),
            ('mention', '@yomgui'),
            ('punct', '#'),
            ('punct', '@')
        ]

    def test_tricky_numbers(self):
        tokenizer = WordTokenizer()

        tokens = list(tokenizer('20m2 747-400 5.6, 6.7 5,6. 6,7 5,6.6,7 5,6,7 10_000 4.5, 5,6 and 2.3.4 and 2.3. and 2.5.5.3. or 4.5.stop'))

        assert tokens == [
            ('word', '20m2'),
            ('word', '747-400'),
            ('number', '5.6'),
            ('punct', ','),
            ('number', '6.7'),
            ('number', '5,6'),
            ('punct', '.'),
            ('number', '6,7'),
            ('number', '5,6'),
            ('punct', '.'),
            ('number', '6,7'),
            ('number', '5,6'),
            ('punct', ','),
            ('punct', '7'),
            ('word', '10_000'),
            ('number', '4.5'),
            ('punct', ','),
            ('number', '5,6'),
            ('word', 'and'),
            ('number', '2.3'),
            ('punct', '.'),
            ('punct', '4'),
            ('word', 'and'),
            ('number', '2.3'),
            ('punct', '.'),
            ('word', 'and'),
            ('number', '2.5'),
            ('punct', '.'),
            ('number', '5.3'),
            ('punct', '.'),
            ('word', 'or'),
            ('number', '4.5'),
            ('punct', '.'),
            ('word', 'stop')
        ]
