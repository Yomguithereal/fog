# =============================================================================
# Fog Cologne Phonetic Algorithm
# =============================================================================
#
# Function computing the Cologne phonetic code for German names.
#
# [Url]:
# https://en.wikipedia.org/wiki/Cologne_phonetics
#
# [Article]:
# Hans Joachim Postel: Die Kölner Phonetik. Ein Verfahren zur Identifizierung
# von Personennamen auf der Grundlage der Gestaltanalyse.
# in: IBM-Nachrichten, 19. Jahrgang, 1969, S. 925-931.
#
import re
from unidecode import unidecode
from fog.utils import squeeze

ALPHA_RE = re.compile(r'[^A-Z]')

CODES = {
    'H': None,

    'A': '0',
    'E': '0',
    'I': '0',
    'O': '0',
    'U': '0',
    'J': '0',
    'Y': '0',

    'B': '1',
    'P': '1',

    'F': '3',
    'V': '3',
    'W': '3',

    'G': '4',
    'K': '4',
    'Q': '4',

    'L': '5',

    'M': '6',
    'N': '6',

    'R': '7',

    'S': '8',
    'Z': '8'
}

DT = set(['C', 'S', 'Z'])
CFOLLOWING1 = set(['A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'])
CFOLLOWING2 = set(['A', 'H', 'K', 'O', 'Q', 'U', 'X'])
CPREVIOUS = set(['S', 'Z'])
X = set(['C', 'Q', 'K'])

GERMANIC_SUBSTITUTIONS = [
    ('Ä', 'A'),
    ('Ö', 'O'),
    ('Ü', 'U'),
    ('ß', 'SS'),
    ('PH', 'F')
]


def cologne(name):
    """
    Function returning the Cologne phonetic code for the given name.

    Args:
        name (string): Name to encode.

    Returns:
        string: The name encoded.

    """

    # Preparing the name
    name = name.upper()

    for p, r in GERMANIC_SUBSTITUTIONS:
        name = name.replace(p, r)

    name = unidecode(name)
    name = re.sub(ALPHA_RE, '', name)

    code = []

    last_i = len(name) - 1

    for i, letter in enumerate(name):
        possible_code = CODES.get(letter)

        if possible_code is not None:
            code.append(possible_code)

        # Handling D/T
        elif letter == 'D' or letter == 'T':
            code.append('8' if i < last_i and name[i + 1] in DT else '2')

        # Handling C
        elif letter == 'C':

            if (
                len(name) > 1 and
                (i == 0 and name[i + 1] in CFOLLOWING1)
                or (i < last_i and name[i + 1] in CFOLLOWING2 and name[i - 1] not in CPREVIOUS)
            ):
                code.append('4')
            else:
                code.append('8')

        # Handling X
        elif letter == 'X':
            code.append('8' if i > 0 and name[i - 1] in X else '48')

    if len(code) == 0:
        return ''

    # Squeezing and dropping not leading 0
    rest = squeeze(''.join(code[1:])).replace('0', '')

    return code[0] + rest
