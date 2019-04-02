# =============================================================================
# Fog Hashjoin Algorithm
# =============================================================================
#
# TODO: Docstring
#
# TODO: check input data length properly
#
#
import warnings
from types import GeneratorType
from pprint import pprint


def hashjoin(left, right, key=None, keys=None):
    """
    Pairs are found across two different datasets : left and right.

    Args
        left (iterable) : Arbitrary iterable containing data points. Will be
            fully consumed.
        right (iterable): Arbitrary iterable containing data points. Will be
            fully consumed.
        key (callable) : A function returning an item's key.
        keys (callable) : A function returning an item's keys.

    Yield
        list: List of simple pairs found across the the two datasets.
    """
    if not (isinstance(left, GeneratorType) and isinstance(right, GeneratorType)):
        if len(left) > len(right):
            warnings.warn(
                'For performance reasons, len(left) should be > to len(right).',
                Warning
            )

    # Single key
    if key is not None:
        for item_l in left:
            key_l = key(item_l)

            for item_r in right:
                key_r = key(item_r)

                if k_left == k_right:
                    yield (item_l, item_r)

    # Multiple keys
    if keys is not None:
        for item_l in left:
            key_l = keys(item_l)

            for item_r in right:
                key_r = keys(item_r)

                if len(list(set(key_l) & set(key_r))) > 0:
                    yield (item_l, item_r)
