# =============================================================================
# Fog Utility Functions
# =============================================================================
#
# Miscellaneous functions used throughout the various module.
#
import re

SQUEEZE_RE = re.compile(r'(?:(.)\1+)')
SQUEEZE_ROMAN_RE = re.compile(r'(?:([^IXCMixcm])\1+)')


def squeeze(string, keep_roman_numerals=False):
    """
    Simple helper dropping consecutive duplicates in a string.

    Args:
        string (string): Target string.
        keep_roman_numerals (boolean, optional): Whether not to squeeze roman
            numerals. Defaults to `False`.

    Returns:
        string: The string, without consecutive duplicates.

    """
    return (SQUEEZE_ROMAN_RE if keep_roman_numerals else SQUEEZE_RE).sub(r'\1', string)
