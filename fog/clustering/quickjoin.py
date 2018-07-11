# =============================================================================
# Fog QuickJoin Clustering
# =============================================================================
#
# Implementation of the Quick Join algorithm that works by recursively
# partitionning the given data with regards to the triangular inequality in
# order to reduce the amount of necessary distance computations.
#
# [Reference]:
# Jacox, Edwin H., et Hanan Samet. « Metric Space Similarity Joins ».
# ACM Transactions on Database Systems 33, no 2 (1 juin 2008): 1‑38.
# https://doi.org/10.1145/1366102.1366104.
#
# Fredriksson K., Braithwaite B. (2013) Quicker Similarity Joins in Metric
# Spaces. In: Brisaboa N., Pedreira O., Zezula P. (eds) Similarity Search and
# Applications. SISAP 2013. Lecture Notes in Computer Science, vol 8199.
# Springer, Berlin, Heidelberg
#
import random
from fog.clustering.utils import clusters_from_pairs


def partition(S, distance, p, radius, rho):
    L = []
    G = []
    Lw = []
    Gw = []

    l = rho - radius
    g = rho + radius

    for item in S:
        d = distance(p, item)

        if d < rho:
            L.append(item)

            if l <= d:
                Lw.append(item)
        else:
            G.append(item)

            if d <= g:
                Gw.append(item)

    return L, G, Lw, Gw


def quickjoin_bruteforce(S1, S2, distance, radius):
    for i in range(len(S1)):
        A = S1[i]

        for j in range(len(S2)):
            B = S2[j]

            if distance(A, B) <= radius:
                yield (A, B)


def quickjoin_self_bruteforce(S, distance, radius):
    n = len(S)

    for i in range(n):
        A = S[i]

        for j in range(i + 1, n):
            B = S[j]

            if distance(A, B) <= radius:
                yield (A, B)


def quickjoin(data, distance, radius, block_size=500,
              min_size=2, max_size=float('inf'),
              mode='connected_components',
              seed=None):
    """
    Function returning an iterator over found clusters using the QuickJoin
    algorithm.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        distance (callable): The distance function to use. Must be a true
            metric, e.g. the Levenshtein distance.
        radius (number, optional): produced clusters' radius.
        block_size (number, optional): block size where the algorithm will
            switch to brute. Defaults to 500.
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

    rng = random.Random(seed)

    if type(data) is not list:
        data = list(data)

    def clustering():
        stack = [(data, None)]

        while len(stack) != 0:
            S1, S2 = stack.pop()

            # QuickJoin procedure
            if S2 is None:

                S = S1
                N = len(S)

                if N <= block_size:
                    yield from quickjoin_self_bruteforce(S, distance, radius)
                    continue

                # Randomly selecting pivots. They must be different
                p1 = rng.randint(0, N - 1)
                p2 = None

                while p2 is None or p1 == p2:
                    p2 = rng.randint(0, N - 1)

                p1 = S[p1]
                p2 = S[p2]

                rho = distance(p1, p2)

                L, G, Lw, Gw = partition(S, distance, p1, radius, rho)

                # Recursion
                stack.append((G, None))
                stack.append((L, None))
                stack.append((Lw, Gw))

            # QuickJoinWin procedure
            else:
                N1 = len(S1)
                N2 = len(S2)
                N = N1 + N2

                if N <= block_size:
                    yield from quickjoin_bruteforce(S1, S2, distance, radius)
                    continue

                p1 = rng.randint(0, N - 1)
                p2 = None

                while p2 is None or p1 == p2:
                    p2 = rng.randint(0, N - 1)

                p1 = S1[p1] if p1 < N1 else S2[p1 - N1]
                p2 = S1[p2] if p2 < N1 else S2[p2 - N1]

                rho = distance(p1, p2)

                L1, G1, Lw1, Gw1 = partition(S1, distance, p1, radius, rho)
                L2, G2, Lw2, Gw2 = partition(S2, distance, p1, radius, rho)

                stack.append((L1, L2))
                stack.append((G1, G2))
                stack.append((Lw1, Gw2))
                stack.append((Gw1, Lw2))

    yield from clusters_from_pairs(
        clustering(),
        min_size=min_size,
        max_size=max_size,
        mode=mode
    )
