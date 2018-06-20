# =============================================================================
# Fog Rusalka
# =============================================================================
#
# Rusalka is a standardization algorithm for transliterated Russian names.
#
import re

FILTER = re.compile(r'[^a-z]')
DUPLICATED = re.compile(r'(.)\1+')
VOWELS = re.compile(r'[aeiouy]')

RULES = [
    (r'i[jy]$', ''),
    (r'[fvw]', 'f'),
    (r'[dt]?[cs]h', 'ʃ'),
    (r'[dt]?(?:zh|j)', 'ʒ'),
    (r'h', '')
]

RULES = [(re.compile(p), r) for p, r in RULES]


def rusalka(name):
    name = name.lower()

    # Dropping irrelevant characters
    name = re.sub(FILTER, '', name)

    # Applying rules
    for pattern, replacement in RULES:
        name = re.sub(pattern, replacement, name)

    # Deduplication
    name = re.sub(DUPLICATED, r'\1', name)

    # Dropping vowels
    name = re.sub(VOWELS, '', name)

    return name
