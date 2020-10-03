# =============================================================================
# Fog Skeleton Key
# =============================================================================
#
# The skeleton key by Pollock and Zamora.
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
VOWELS = set('AEIOU')


def skeleton_key(string):
    """
    Function returning a string's skeleton key which is constructed thusly:

    1. The first letter of the string
    2. Unique consonants in order of appearance
    3. Unique vowels in order of appearance

    This key is very useful when searching for mispelled strings because
    if sorted using this key, similar strings will be next to each other.

    Args:
        string (str): The string to encode.

    Returns:
        string: The string's skeleton key.

    """

    # Deburring
    string = unidecode(string)

    # Normalizing case
    string = string.upper()

    # Dropping useless characters
    string = re.sub(UNDESIRABLES_RE, '', string)

    # Composing the key
    if not string:
        return ''

    first_letter = string[0]
    key = [first_letter]

    consonants = set()
    vowels = set()

    for i in range(1, len(string)):
        letter = string[i]

        if letter == first_letter:
            continue

        if letter in VOWELS:
            if letter not in vowels:
                vowels.add(letter)
                key.append(letter)
        else:
            if letter not in consonants:
                consonants.add(letter)
                key.insert(len(key) - len(vowels), letter)

    return ''.join(key)
