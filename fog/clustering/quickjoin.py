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
# [Notes]:
# From what I could gather right now, Fredriksson K., Braithwaite B. methods
# to improve the algorithm don't really work with my use-case. For instance,
# the book-keeping of the join_pivots methods takes more time than the
# saved distance computations, even with a eta parameter set to a high value.
# I will need to test examples where the distance is more expensive (e.g.,
# testing with quite tiny strings, the Levensthein distance is not really
# prohibitive right now).
#
# Using a Vantage Point Tree does not yield faster results neither.
#
import dill
import random
from multiprocessing import Pool
from phylactery import VPTree

from fog.clustering.utils import clusters_from_pairs

# TODO: implement the eta parameter


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


def quickjoin_vptree(S1, S2, distance, radius):

    # Indexing the smallest set
    if len(S1) > len(S2):
        S1, S2 = S2, S1

    if len(S1) == 1:
        B = S1[0]

        for A in S2:
            if distance(A, B) <= radius:
                yield (A, B)
    else:
        tree = VPTree(S1, distance)

        for A in S2:
            for B, d in tree.neighbors_in_radius(A, radius):
                yield (A, B)


def quickjoin_self_vptree(S, distance, radius):

    if len(S) == 1:
        return

    tree = VPTree(S, distance)

    for A in S:
        for B, d in tree.neighbors_in_radius(A, radius):
            if A == B:
                continue

            if id(A) < id(B):
                yield (A, B)


def quickjoin_join_pivots(S1, S2, distance, radius):
    """
    From Fredriksson & Braithwaite. Algorithm 5.

    """

    N1 = len(S1)
    N2 = len(S2)

    k = max(1, min(16, N1 // 8))

    P = [0] * N2 * k

    for i in range(k):
        A = S1[i]

        for j in range(N2):
            B = S2[j]
            d = distance(A, B)
            P[i * N2 + j] = d

            if d <= radius:
                yield (A, B)

    D = [0] * k

    for i in range(k, N1):
        A = S1[i]

        for l in range(k):
            D[l] = distance(S1[l], A)

        for j in range(N2):
            B = S2[j]
            f = False

            for l in range(k):
                if abs(P[l * N2 + j] - D[l]) > radius:
                    f = True
                    break

            if not f and distance(A, B) <= radius:
                yield (A, B)


def select_block_functions(vp_tree):
    if vp_tree:
        return quickjoin_vptree, quickjoin_self_vptree

    return quickjoin_bruteforce, quickjoin_self_bruteforce


def worker(payload):
    distance, radius, S1, S2, vp_tree = payload

    distance = dill.loads(distance)

    BF, SBF = select_block_functions(vp_tree)

    if S2 is None:
        return list(SBF(S1, distance, radius))

    return list(BF(S1, S2, distance, radius))


def quickjoin(data, radius, distance=None, similarity=None, block_size=500,
              min_size=2, max_size=float('inf'),
              mode='connected_components',
              seed=None, processes=1, beta=1.0, vp_tree=False):
    """
    Function returning an iterator over found clusters using the QuickJoin
    algorithm.

    Note that this algorithm returns the same result as pairwise computations
    would.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        distance (callable): The distance function to use. Must be a true
            metric, e.g. the Levenshtein distance.
        similarity (callable): The similarity function to use. Must be a true
            metric, e.g. the Jaccard similarity.
        radius (number): produced clusters' radius.
        block_size (number, optional): block size where the algorithm will
            switch to brute. Defaults to 500.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.
        seed (number, optional): Seed for RNG. Defaults to None.
        processes (number, optional): Number of processes to use.
            Defaults to 1.
        beta (number, optional): Balancing parameter from Fredriksson &
            Braithwaite. Defaults to no-op 1.0.
        vp_tree (bool, optional): Whether to use Vantage Point Trees to solve
            blocks. Defaults to False.

    Yields:
        list: A viable cluster.

    """

    rng = random.Random(seed)

    if type(data) is not list:
        data = list(data)

    if similarity is not None:
        distance = lambda x, y: -similarity(x, y)
        radius = -radius

    # Iterator recursively partitioning the data set using QuickJoin's method
    def blocks():
        stack = [(data, None)]

        # "Recursivity" through stack
        while len(stack) != 0:
            S1, S2 = stack.pop()

            # QuickJoin procedure
            if S2 is None:

                S = S1
                N = len(S)

                if N <= block_size:
                    yield (S, None)
                    continue

                # Randomly selecting pivots. They must be different
                p1 = rng.randint(0, N - 1)
                p2 = None

                while p2 is None or p1 == p2:
                    p2 = rng.randint(0, N - 1)

                p1 = S[p1]
                p2 = S[p2]

                rho = beta * distance(p1, p2)

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

                    if N1 == 0 or N2 == 0:
                        continue

                    yield (S1, S2)
                    continue

                # Randomly selecting pivots. They must be different
                p1 = rng.randint(0, N - 1)
                p2 = None

                while p2 is None or p1 == p2:
                    p2 = rng.randint(0, N - 1)

                p1 = S1[p1] if p1 < N1 else S2[p1 - N1]
                p2 = S1[p2] if p2 < N1 else S2[p2 - N1]

                rho = beta * distance(p1, p2)

                L1, G1, Lw1, Gw1 = partition(S1, distance, p1, radius, rho)
                L2, G2, Lw2, Gw2 = partition(S2, distance, p1, radius, rho)

                stack.append((L1, L2))
                stack.append((G1, G2))
                stack.append((Lw1, Gw2))
                stack.append((Gw1, Lw2))

    # Iterator performing bruteforce distance computation over found blocks
    def clustering():

        BF, SBF = select_block_functions(vp_tree)

        for S1, S2 in blocks():
            if S2 is None:
                yield from SBF(S1, distance, radius)
            else:
                yield from BF(S1, S2, distance, radius)

    def clustering_parallel():
        with Pool(processes=processes) as pool:
            pickled_distance = dill.dumps(distance)

            pool_iter = (
                (pickled_distance, radius, S1, S2, vp_tree)
                for S1, S2 in blocks()
            )

            for pairs in pool.imap_unordered(worker, pool_iter):
                yield from pairs

    yield from clusters_from_pairs(
        clustering() if processes == 1 else clustering_parallel(),
        min_size=min_size,
        max_size=max_size,
        mode=mode,
        fuzzy=True
    )
