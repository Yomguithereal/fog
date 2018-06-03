# =============================================================================
# Fog Clustering Utilities
# =============================================================================
#
# Miscellaneous redundant functions used by clustering routines.
#


def make_similarity_function(similarity=None, distance=None, radius=None):
    if similarity is None and distance is None:
        raise TypeError('fog.clustering: need at least a similarity or distance function.')

    if radius:
        if similarity:
            return lambda A, B: similarity(A, B) <= radius
        else:
            return lambda A, B: distance(A, B) <= radius
    else:
        if similarity:
            return similarity
        else:
            return lambda A, B: not distance(A, B)
