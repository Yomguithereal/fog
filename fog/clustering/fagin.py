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
# https://arxiv.org/pdf/1011.2807.pdf
# https://nlp.stanford.edu/IR-book/html/htmledition/contents-1.html
#
import math
from random import shuffle
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
        best = None
        t_vector = {}

        while True:
            stop = True

            for d in vector:
                l = inverted_lists[d]

                if offset >= len(l):
                    continue

                stop = False

                w, j = l[offset]

                if i == j:

                    # TODO: probably ned to reset stop to take edge case into account
                    offset2 = offset + 1

                    if offset2 >= len(l):
                        continue

                    w, j = l[offset2]

                t_vector[d] = w

                if j in visited:
                    continue

                cs = sparse_cosine_similarity(vector, vectors[j])
                visited.add(j)

                if best is None or cs > best[0]:
                    best = (cs, j)

            # Final break + return self if best cos is 0.0
            if stop:
                yield i, best[1] if best is not None else i
                break

            t = sparse_cosine_similarity(vector, t_vector)

            if best is not None and best[0] >= t:
                yield i, best[1] if best is not None else i
                break

            offset += 1


def naive_cosine_pairs(vectors):
    inverted_lists = defaultdict(list)

    for i, vector in enumerate(vectors):
        visited = set()

        for d in vector:
            l = inverted_lists[d]

            for j in l:
                if j in visited:
                    continue

                visited.add(j)

                yield i, j

            l.append(i)


def sqrt_indexation_pairs(vectors):
    indices = list(range(len(vectors)))
    shuffle(indices)

    leaders_count = int(math.sqrt(len(vectors)))

    leaders = indices[:leaders_count]

    proximities = defaultdict(list)

    for i, v in enumerate(vectors):
        leader = min(leaders, key=lambda x: 1.0 - sparse_cosine_similarity(v, vectors[x]))

        yield i, leader

        l = proximities[leader]

        for j in l:
            yield i, j

        l.append(i)
