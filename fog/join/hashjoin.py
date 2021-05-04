# =============================================================================
# Fog Hashjoin Algorithm
# =============================================================================
#
# TODO: key(s) as iterable of fuctions ?
#
from types import GeneratorType
import warnings


def hashjoin(left, right, key=None, keys=None):
    """
    For each element in left, hasjoin finds similar elements in right.
    Pairs are yieled when two elements share at least one key.

    Returns a list of pair of candidates (left_elt, right_elt).

    Args
        left (iterable): Arbitrary iterable containing data points. Will be
            fully consumed.
        right (iterable): Arbitrary iterable containing data points. Will be
            fully consumed.
        key (function): Functions returning an item's key.
        keys (function): Functions returning an item's keys.

    Yield
        (list): List of pairs found across left and right datasets.
    """
    try:
        if len(left) > len(right):
            A, B = right, left
            invert = True
        else:
            A, B = left, right
            invert = False
    except TypeError:
        A, B = left, right
        invert = False

    if isinstance(B, GeneratorType):
        warnings.warn(
            """
            fog.join.hasjoin: At least one of the input iterables is a
            generator. It will be fully consumed before hasjoin finds all
            similar pairs.
            """)

    # Single key
    if key is not None:
        for a in A:
            key_a = key(a)

            for b in B:
                key_b = key(b)

                if key_a == key_b:

                    if invert:
                        yield (b, a)
                    else:
                        yield (a, b)

    # Multiple keys
    if keys is not None:
        for a in A:
            key_a = keys(a)

            for b in B:
                key_b = keys(b)

                if len(list(set(key_a) & set(key_b))) > 0:

                    if invert:
                        yield (b, a)
                    else:
                        yield (a, b)
