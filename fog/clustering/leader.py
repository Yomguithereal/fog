# =============================================================================
# Fog Leader Clustering
# =============================================================================
#
# Clustering algorithm based on the fact that one can sometimes consider the
# similarity relation as transitive (A =~ B, B =~ C means that A =~ C).
#
# This means that finding clusters is just a matter of building a similarity
# graph by computing pairwise distances and extracting its connected components
# as clusters.
#
# This method is very efficient in cases when the graph only contains few
# components because it helps cutting down the quadratic nature of pairwise
# distance computations (one will only compare items to the "leader" of their
# components).
#
# However, in the record-linkage case, this does not cut much computations
# because the resulting graph often has a multitude of tiny components.
#
from phylactery import UnionFind
from fog.clustering.utils import make_similarity_function


def leader(data, similarity=None, distance=None, radius=None,
           min_size=2, max_size=float('inf')):
    """
    Function returning an iterator over found clusters using the "Leader"
    method, relying on connected component of the computed distance graph.

    Runs in O(c * (c - 1) / 2), i.e. O(c^2), c being the number of found
    components.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        similarity (callable): If radius is specified, a function returning
            the similarity between two points. Else, a function returning
            whether two points should be deemed similar. Alternatively, one can
            specify `distance` instead.
        distance (callable): If radius is specified, a function returning
            the distance between two points. Else, a function returning
            whether two point should not be deemed similar. Alternatively, one
            can specify `similarity` instead.
        radius (number, optional): produced clusters' radius.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # We need to consume as a list to be able of random access
    if type(data) is not list:
        data = list(data)

    n = len(data)
    sets = UnionFind(n)

    # Computing pairwise distances
    for i in range(n):
        A = data[i]
        A_root = sets.find(i)

        for j in range(i + 1, n):
            B = data[j]
            B_root = sets.find(j)

            if A_root == B_root:
                continue

            if similarity(A, B):
                sets.union(i, j)

    # Iterating over found components
    for component in sets.components(min_size=min_size, max_size=max_size):
        yield [data[i] for i in component]
