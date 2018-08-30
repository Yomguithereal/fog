# =============================================================================
# Fog Miscellaneous Keys Unit Tests
# =============================================================================
from fog.key import ngram_keys

TEST = [
    (
        'smith',
        ['smmiitth', 'smmiit', 'smmith', 'smitth', 'miitth'],
        ['smmi', 'smit', 'smth', 'miit', 'mith', 'itth']
    ),
    (
        'smithy',
        ['smmiitthhy', 'smmiitth', 'smmiithy', 'smmithhy', 'smitthhy', 'miitthhy'],
        ['smmiit', 'smmith', 'smmihy', 'smitth', 'smithy', 'smthhy', 'miitth', 'miithy', 'mithhy', 'itthhy']
    ),
    (
        'smithe',
        ['smmiitthhe', 'smmiitth', 'smmiithe', 'smmithhe', 'smitthhe', 'miitthhe'],
        ['smmiit', 'smmith', 'smmihe', 'smitth', 'smithe', 'smthhe', 'miitth', 'miithe', 'mithhe', 'itthhe']
    )
]


class TestMiscKeys(object):
    def test_ngram_keys(self):

        for word, k1, k2 in TEST:
            k = list(ngram_keys(2, word))

            assert k == k1

            k = list(ngram_keys(2, word, threshold=1.0))

            assert k == [k1[0]]

            k = list(ngram_keys(2, word, threshold=0.7))

            assert k == k1 + k2
