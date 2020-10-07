# =============================================================================
# Fog Fagin Clustering
# =============================================================================
#
# Miscellaneous functions related to Fagin's algorithms in order to perform
# top k queries and such.
#
# [Articles]:
# Optimal aggregation algorithms for middleware
# Ronald Fagin, Amnon Lotem, and Moni Naor
#
# Combining Fuzzy Information from Multiple Systems
# Ronald Fagin
#
# Index-based, High-dimensional, Cosine Threshold Querying with Optimality
# Guarantees. Yuliang Li, Jianguo Wang, Benjamin Pullman, Nuno Bandeira, and
# Yannis Papakonstantinou
#
# [References]:
# http://homepages.inf.ed.ac.uk/libkin/teach/dataintegr09/topk.pdf
# http://alumni.cs.ucr.edu/~skulhari/Top-k-Query.pdf
#
from collections import defaultdict, Counter

from fog.metrics.cosine import sparse_cosine_similarity


def fagin_k1(vectors):
    inverted_lists = defaultdict(list)

    for i, vector in enumerate(vectors):
        for d, w in vector.items():
            inverted_lists[d].append((w, i))

    for l in inverted_lists.values():
        l.sort()

    for i, vector in enumerate(vectors):
        counts = Counter()
        offset = 0

        D = len(vector)

        while True:
            stop = True

            for d in vector:
                l = inverted_lists[d]

                if offset < len(l):
                    counts[l[offset][1]] += 1
                    stop = False

            if stop:
                break

            if sum(1 for c in counts.values() if c >= D) >= 2:
                yield i, list(j for j in counts.keys() if j != i)
                break

            offset += 1


def threshold_algorithm_k1(vectors):
    inverted_lists = defaultdict(list)

    for i, vector in enumerate(vectors):
        for d, w in vector.items():
            inverted_lists[d].append((w, i))

    for l in inverted_lists.values():
        l.sort()

    for i, vector in enumerate(vectors):
        visited = set()
        offset = 0

        t = 0.0
        best = [None, None]
        t_vector = {}

        while True:
            stop = True

            for d in vector:
                l = inverted_lists[d]

                if offset >= len(l):
                    continue

                stop = False

                w, j = l[offset]
                t_vector[d] = w

                if j in visited:
                    continue

                cs = sparse_cosine_similarity(vector, vectors[j])
                visited.add(j)

                if best[0] is None:
                    best[0] = (cs, j)
                else:
                    if cs > best[0][0]:
                        best[1] = best[0]
                        best[0] = (cs, j)
                    else:
                        if best[1] is None:
                            best[1] = (cs, j)
                        elif cs > best[1][0]:
                            best[1] = (cs, j)

            # Final break + return self if best cos is 0.0
            if stop:
                yield i, best[1][1] if best[1] is not None else best[0][1]
                break

            t = sparse_cosine_similarity(vector, t_vector)

            if best[1] is not None and best[1][0] >= t:
                yield i, best[1][1] if best[1] is not None else best[0][1]
                break

            offset += 1
