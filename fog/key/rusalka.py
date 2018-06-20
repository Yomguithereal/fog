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

RULES = [
    (r'i[jy]$', ''),
    (r'[fvw]', 'f'),
    (r'[dt]?[cs]h|tz', 'ʃ'),
    (r'[dt]?(?:zh|j)', 'ʒ'),
    (r'ks', 'x'),
    (r'^y?e', 'j'),
    (r'^y(?=[aeiou])|iou', 'j'),
    (r'[cg]', 'k'),
    (r'h', '')
]

RULES = [(re.compile(p), r) for p, r in RULES]


def rusalka(name):

    # Lower case
    name = name.lower()

    # Unidecode
    name = unidecode(name)

    # Dropping irrelevant characters
    name = re.sub(FILTER, '', name)

    # Applying rules
    for pattern, replacement in RULES:
        name = re.sub(pattern, replacement, name)

    # Deduplication
    name = re.sub(DUPLICATED, r'\1', name)

    first_letter = name[0]
    rest = name[1:]

    # Dropping vowels
    rest = re.sub(VOWELS, '', rest)

    # Handling first letter
    if re.match(VOWELS, first_letter):
        first_letter = 'a'

    return first_letter + rest
