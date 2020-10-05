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
# [Notes]:
# Recall is a function of the k parameter. k is also intimately related
# to the data's intrisic's dimensionality. One should increase k to increase
# recall, at the cost of poorer performance. Chosing log2(n) as k seems to
# be a generally good compromise.
#
import math
import random
from heapq import heapify, heapreplace
from fog.clustering.utils import clusters_from_pairs

# TODO: parallelize nn_descent_full


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


def nn_descent(data, radius, similarity=None, distance=None, k=None,
               min_size=2, max_size=float('inf'),
               mode='connected_components',
               seed=None):
    """
    Function returning an iterator over found clusters using the NN-Descent
    algorithm.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        radius (number): produced clusters' radius.
        k (number, optional): number of nearest neighbor to find per item.
            If not given, k will default to log2(n).
        similarity (callable): If radius is specified, a function returning
            the similarity between two points. Else, a function returning
            whether two points should be deemed similar. Alternatively, one can
            specify `distance` instead.
        distance (callable): If radius is specified, a function returning
            the distance between two points. Else, a function returning
            whether two point should not be deemed similar. Alternatively, one
            can specify `similarity` instead.
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

    # Chosing k
    if k is None:
        k = int(math.log2(N))

    # Initial samples
    for i, item in enumerate(V):
        neighbors = [(similarity(item, V[j]), j) for j in sample(rng, N, k, i)]
        heapify(neighbors)
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
                        heapreplace(B[i], (s, jj))

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


def shuffle_k(rng, L, k):
    i = -1
    last_i = len(L) - 1

    while i < k - 1:
        i += 1

        r = rng.randint(i, last_i)
        v = L[r]

        L[r] = L[i]
        L[i] = v


def sample_full(rng, L, k):
    """
    Function sampling k indices from given list.

    """

    N = len(L)

    if N <= k:
        return list(L)

    shuffle_k(rng, L, k)

    return L[0:k]


def reverse_full(old, new):
    """
    Returns the list of in-neighbors from the list of out-neighbors.

    """
    old_prime = [[] for _ in range(len(old))]
    new_prime = [[] for _ in range(len(new))]

    for i in range(len(old)):
        for j in old[i]:
            old_prime[j].append(i)
        for j in new[i]:
            new_prime[j].append(i)

    return old_prime, new_prime


def nn_descent_full(data, radius, similarity=None, distance=None, k=None,
                    min_size=2, max_size=float('inf'),
                    mode='connected_components',
                    seed=None, rho=0.5, delta=0.001):
    """
    Function returning an iterator over found clusters using the NN-Descent Full
    algorithm.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        radius (number): produced clusters' radius.
        k (number, optional): number of nearest neighbor to find per item.
            If not given, k will default to log2(n).
        similarity (callable): If radius is specified, a function returning
            the similarity between two points. Else, a function returning
            whether two points should be deemed similar. Alternatively, one can
            specify `distance` instead.
        distance (callable): If radius is specified, a function returning
            the distance between two points. Else, a function returning
            whether two point should not be deemed similar. Alternatively, one
            can specify `similarity` instead.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.
        seed (number, optional): Seed for RNG. Defaults to None.
        rho (number, optional): rho parameter, or sample rate, defining a
            trade-off between accuracy and speed. The lower this number is,
            the faster it runs, but the less accurate it is. Defaults
            to 0.5.
        delta (number, optional): early termination threshold. Roughly the
            fraction of try K-NN that are allowed to be missed due an early
            termination. Defaults to 0.001.

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

    # Chosing k
    if k is None:
        k = int(math.log2(N))

    NK = N * k
    rhoK = int(rho * k)

    # Initial samples
    for i, item in enumerate(V):
        neighbors = [(similarity(item, V[j]), j, True) for j in sample(rng, N, k, i)]
        heapify(neighbors)
        B.append(neighbors)

    c = NK

    while c >= delta * NK:
        old = []
        new = []

        for i, item in enumerate(V):
            o = set()
            n = []

            for j, neighbor in enumerate(B[i]):
                if not neighbor[2]:
                    o.add(neighbor[1])
                else:
                    n.append((j, neighbor[1]))

            # Sampling rhoK from new
            s = sample_full(rng, n, rhoK)
            sample_set = set(s)

            for k in n:
                if k not in sample_set:
                    B[i][k[0]] = B[i][k[0]][0:2] + (False, )

            old.append(o)
            new.append(set([index for _, index in s]))

        old_prime, new_prime = reverse_full(old, new)

        c = 0

        for i, item in enumerate(V):
            o = old[i]
            n = new[i]

            o.update(sample_full(rng, old_prime[i], rhoK))
            n.update(sample_full(rng, new_prime[i], rhoK))

            for u1 in n:

                for u2 in n:
                    if u1 >= u2:
                        continue

                    s = similarity(V[u1], V[u2])

                    if s > B[u1][0][0]:
                        c += 1
                        heapreplace(B[u1], (s, u2, True))

                    if s > B[u2][0][0]:
                        c += 1
                        heapreplace(B[u2], (s, u1, True))

                for u2 in o:

                    if u1 == u2:
                        continue

                    s = similarity(V[u1], V[u2])

                    if s > B[u1][0][0]:
                        c += 1
                        heapreplace(B[u1], (s, u2, True))

                    if s > B[u2][0][0]:
                        c += 1
                        heapreplace(B[u2], (s, u1, True))

    def clustering():
        for i, neighbors in enumerate(B):
            for s, j, _ in neighbors:
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
