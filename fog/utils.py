# =============================================================================
# Fog Utils
# =============================================================================
#
# Miscellaneous functions used throughout the library.
#
import math


def upper_triangular_matrix_chunk_iter(data, chunk_size):
    """
    Function returning an iterator over chunks of an upper triangular matrix.
    It's a useful utility to parallelize pairwise distance computations, for
    instance.

    Args:
        data (iterable): The matrix's data.
        chunk_size (int): Size of the chunks to yield.

    Yields:
        tuple of slices: A matrix's chunk.

    """
    n = len(data)
    c = math.ceil(n / chunk_size)

    for j in range(c):
        j_offset = j * chunk_size
        j_limit = j_offset + chunk_size

        for i in range(0, min(j + 1, c)):
            i_offset = i * chunk_size
            i_limit = i_offset + chunk_size

            yield (
                data[i_offset:i_limit],
                data[j_offset:j_limit],
                i_offset,
                j_offset
            )
