# =============================================================================
# Fog Utility Functions
# =============================================================================
#
# Miscellaneous functions used throughout the various module.
#
import re

SQUEEZE_RE = re.compile(r'(?:(.)\1+)')


def squeeze(string):
    """
    Simple helper dropping consecutive duplicates in a string.

    Args:
        string (string): Target string.

    Returns:
        string: The string, without consecutive duplicates.

    """
    return SQUEEZE_RE.sub(r'\1', string)
