# =============================================================================
# Fog Omission Key
# =============================================================================
#
# The omission key by Pollock and Zamora.
#
# [Urls]:
# http://dl.acm.org/citation.cfm?id=358048
# http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.12.385&rep=rep1&type=pdf
#
# [Reference]:
# Pollock, Joseph J. and Antonio Zamora. 1984. "Automatic Spelling Correction
# in Scientific and Scholarly Text." Communications of the ACM, 27(4).
# 358--368.
import re
from unidecode import unidecode

UNDESIRABLES_RE = re.compile(r'[^A-Z]')
CONSONANTS = 'JKQXZVWYBFMGPDHCLNTSR'
VOWELS = set('AEIOU')


def omission_key(string):
    """
    Function returning a string's omission key which is constructed thusly:

    1. First we record the string's set of consonant in an order
       where most frequently mispelled consonants will be last.
    2. Then we record the string's set of vowels in the order of
       first appearance.

    This key is very useful when searching for mispelled strings because
    if sorted using this key, similar strings will be next to each other.

    Args:
        string (str): The string to encode.

    Returns:
        string: The string's omission key.

    """

    # Deburring
    string = unidecode(string)

    # Normalizing case
    string = string.upper()

    # Dropping useless characters
    string = re.sub(UNDESIRABLES_RE, '', string)

    if not string:
        return ''

    # Composing the key
    letters = set()
    consonants = []
    vowels = []

    # Adding vowels in order they appeared
    for letter in string:
        if letter in VOWELS and letter not in vowels:
            vowels.append(letter)
        else:
            letters.add(letter)

    # Adding consonants in order
    for consonant in CONSONANTS:
        if consonant in letters:
            consonants.append(consonant)

    return ''.join(consonants + vowels)
