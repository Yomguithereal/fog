# =============================================================================
# Fog Phonetics Utility Functions
# =============================================================================
#
# Miscellaneous functions used throughout the phonetics module.
#
import re

SQUEEZE_RE = re.compile(r'(?:(.)\1+)')


def squeeze(string):
    return SQUEEZE_RE.sub(r'\1', string)
