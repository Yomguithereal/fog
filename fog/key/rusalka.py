# =============================================================================
# Fog Rusalka
# =============================================================================
#
# Rusalka is a standardization algorithm for transliterated Russian names.
#
import re
from unidecode import unidecode

FILTER = re.compile(r'[^a-z]')
DUPLICATED = re.compile(r'(.)\1+')
VOWELS = re.compile(r'[aeiouy]')

PHONETIC_NOTATION_RULES = [
    (r'[čšŝ]', 'ch'),
    (r'û', 'iou'),
    (r'ž', 'zh')
]

RULES = [
    (r'cz', 'ts'),
    (r'i[jy]$', ''),
    (r'[fvw]|ph', 'f'),
    (r'^[jy]?e', 'J'),
    (r'[dt]?[cs]h|tz', 'ʃ'),
    (r'[dt]?(?:zh|j)', 'ʒ'),
    (r'ks', 'x'),
    (r'^y(?=[aeiou])|iou', 'j'),
    (r'[cg]', 'k'),
    (r'h', '')
]

RULES = [(re.compile(p), r) for p, r in RULES]


def rusalka(name):

    # Lower case
    name = name.lower()

    # Applying phonetic notation rules
    for pattern, replacement in PHONETIC_NOTATION_RULES:
        name = re.sub(pattern, replacement, name)

    # Unidecode
    name = unidecode(name)

    # Dropping irrelevant characters
    name = re.sub(FILTER, '', name)

    # Applying rules
    for pattern, replacement in RULES:
        name = re.sub(pattern, replacement, name)

    # Deduplication
    name = re.sub(DUPLICATED, r'\1', name)
    name = name.lower()

    first_letter = name[0]
    rest = name[1:]

    # Dropping vowels
    rest = re.sub(VOWELS, '', rest)

    # Handling first letter
    if re.match(VOWELS, first_letter):
        first_letter = 'a'

    return first_letter + rest
