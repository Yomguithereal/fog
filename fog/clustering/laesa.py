# =============================================================================
# Fog LAESA Clustering
# =============================================================================
#
# Implementation of the linear AESA algorithm to perform nearest neighbor
# clustering.
#
# [References]:
# Micó, María Luisa, José Oncina, et Enrique Vidal. « A New Version of the
# Nearest-Neighbour Approximating and Eliminating Search Algorithm (AESA) with
# Linear Preprocessing Time and Memory Requirements ». Pattern Recognition
# Letters 15, no 1 (janvier 1994): 9‑17.
# https://doi.org/10.1016/0167-8655(94)90095-7.
#
# Rico-Juan, Juan Ramón, et Luisa Micó. « Comparison of AESA and LAESA Search
# Algorithms Using String and Tree-Edit-Distances ». Pattern Recognition
# Letters 24, no 9‑10 (juin 2003): 1417‑26.
# https://doi.org/10.1016/S0167-8655(02)00382-3.
#
# [Urls]:
# http://www.xavierdupre.fr/app/mlstatpy/helpsphinx/c_ml/kppv.html
#
# Note that this method is not particularly efficient for the general use
# case. It's often worse than the quadratic approach.
#
import math
import random

from fog.clustering.utils import clusters_from_pairs


def pivot_selection(rng, data, pivots, distance):
    """
    Function in charge of pivot selection.

    """
    b_prime = rng.randint(0, len(data) - 1)
    n = len(data)
    p = set()
    A = [0] * n
    D = []

    # Finding pivots
    for i in range(pivots):
        maximum = 0
        b = b_prime
        D.append([0] * n)
        pivot = data[b]

        for j, item in enumerate(data):
            if j in p:
                continue

            d = distance(pivot, item)
            A[j] += d

            if A[j] > maximum:
                b_prime = j
                maximum = A[j]

        p.add(b_prime)

    p = list(p)

    # Pre-computing distances (not necessary, can be done before or later)
    for i in range(pivots):
        pivot = data[p[i]]

        for j, item in enumerate(data):
            D[i][j] = distance(pivot, item)

    return p, D


# TODO: currently not working
def laesa(data, distance, radius, pivots=None, min_size=2,
          max_size=float('inf'), seed=None, mode='connected_components'):
    """
    Function returning an iterator over found clusters using the LAESA method.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        distance (callable): Distance function to be used.
        radius (number): produced clusters' radius.
        pivots (number, optional): number of pivots to use. Defaults to
            log2(n).
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.
        seed (number, optional): rng seed. Defaults to None.
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.

    Yield:
        list: A viable cluster.

    """

    # Building rng
    rng = random.Random(seed)

    # We need to consume as a list to be able of random access
    if type(data) is not list:
        data = list(data)

    # Finding the number of pivots
    if pivots is None:
        pivots = math.ceil(math.log2(len(data)))

    # Finding good pivots
    p, D = pivot_selection(rng, data, pivots, distance)
    n = len(data)

    def clustering():
        DD = 0
        for i, x in enumerate(data):

            # Distance to the nearest pivot
            d_star = float('inf')

            for j in range(pivots):
                d = distance(data[p[j]], x)

                if d < d_star:
                    d_star = d

            for k in range(i + 1, n):

                compute = True

                for j in range(pivots):
                    delta = abs(D[j][i] - D[j][k])

                    if delta > d_star:
                        compute = False
                        break

                if compute:
                    d = distance(x, data[k])
                    DD += 1

                    if d <= radius:
                        yield (x, data[k])

        print('DISTANCES: %i' % DD)

    yield from clusters_from_pairs(
        clustering(),
        min_size=min_size,
        max_size=max_size,
        mode=mode
    )
