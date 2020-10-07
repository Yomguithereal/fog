# =============================================================================
# Fog Fagin Clustering
# =============================================================================
#
# Miscellaneous functions related to Fagin's algorithms in order to perform
# top k queries and such.
#
from collections import defaultdict, Counter


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
