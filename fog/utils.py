# =============================================================================
# Fog Utility Functions
# =============================================================================
#
# Miscellaneous functions used throughout the various module.
#
import re
from statistics import StatisticsError

SQUEEZE_RE = re.compile(r'(.)\1+')
SQUEEZE_ROMAN_RE = re.compile(r'([^IXCMixcm])\1+')


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


class OnlineMean(object):
    """
    Just a helper class to compute the mean of a stream of values online and
    only using constant memory.

    Note that it might be subject to float precision issues.
    """

    __slots__ = ('_sum', '_n')

    def __init__(self):
        self._sum = 0
        self._n = 0

    def add(self, x):
        self._n += 1
        self._sum += x

    def subtract(self, x):
        assert self._n != 0
        self._n -= 1
        self._sum -= x

    def __add__(self, other):
        new = self.__class__()
        new.__iadd__(self)
        new.__iadd__(other)

        return new

    def __iadd__(self, other):
        if not isinstance(other, OnlineMean):
            raise TypeError

        self._n += other._n
        self._sum += other._sum

        return self

    def __len__(self):
        return self._n

    def peek(self):
        if self._n == 0:
            raise StatisticsError

        return self._sum / self._n

    def __float__(self):
        return self.peek()
