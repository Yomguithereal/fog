# =============================================================================
# Fog NN-Descent Clustering
# =============================================================================
#
# Implementation of the probabilistic NN-Descent algorithm able to build
# an approximate k-nn graph from a dataset in subquadratic time.
#
# [Reference]:
# Dong, Wei, Charikar Moses, et Kai Li. « Efficient K-Nearest Neighbor Graph
# Construction for Generic Similarity Measures », 577. ACM Press, 2011.
# https://doi.org/10.1145/1963405.1963487.
#
import heapq
import random
from fog.clustering.utils import make_similarity_function, clusters_from_pairs

# TODO: implement the "full" version


def sample(rng, N, k, i):
    """
    Function sampling k indices from the range 0-N without the i index.

    """

    S = set()

    while len(S) < k:
        random_index = rng.randint(0, N - 1)

        if random_index == i:
            continue

        S.add(random_index)

    return list(S)


def reverse(B):
    """
    Returns the list of in-neighbors from the list of out-neighbors.

    """
    R = [[] for _ in range(len(B))]

    for i, neighbors in enumerate(B):
        for _, j in neighbors:
            R[j].append(i)

    return R


def nn_descent(data, similarity=None, distance=None, k=5, radius=None,
               min_size=2, max_size=float('inf'),
               mode='connected_components',
               seed=None):
    """
    Function returning an iterator over found clusters using the NN-Descent
    algorithm.

    The issue of this algorithm is that you need to increase k to increase
    recall and increasing k increases time complexity towards O(n^2).

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        k (number, optional): number of nearest neighbor to find per item.
            Defaults to 5.
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
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.
        seed (number, optional): Seed for RNG. Defaults to None.

    Yields:
        list: A viable cluster.

    """

    # Seeding rng
    rng = random.Random(seed)

    # Inverting distance if needed
    if distance is not None:
        similarity = lambda x, y: -distance(x, y)
        radius = -radius

    # Making data set into indexable list
    if type(data) is not list:
        data = list(data)

    # Note that B & R could be flat arrays
    V = data
    B = []
    N = len(V)

    def min_similarity_key(x):
        return x[1][1]

    # Initial samples
    for i, item in enumerate(V):
        neighbors = [(similarity(item, V[j]), j) for j in sample(rng, N, k, i)]
        heapq.heapify(neighbors)
        B.append(neighbors)

    c = 1

    while c != 0:
        R = reverse(B)
        C = []

        c = 0

        for i, item in enumerate(V):
            candidates = set(j for _, j in B[i])
            candidates.update(R[i])

            C.append(list(candidates))

        for i in range(N):
            BA = C[i]

            for ii in BA:
                BB = C[ii]

                for jj in BB:

                    if i == jj:
                        continue

                    s = similarity(V[i], V[jj])

                    if s > B[i][0][0]:
                        c += 1
                        heapq.heapreplace(B[i], (s, jj))

    def clustering():
        for i, neighbors in enumerate(B):
            for s, j in neighbors:
                if s >= radius:
                    yield (i, j)

    gen = clusters_from_pairs(
        clustering(),
        min_size=min_size,
        max_size=max_size,
        mode=mode,
        fuzzy=True
    )

    for cluster in gen:
        yield [V[i] for i in cluster]
