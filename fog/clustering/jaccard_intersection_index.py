# =============================================================================
# Fog Key Jaccard Intersection Clustering
# =============================================================================
#
# Clustering routine leveraging an intersection index to find similar items.
#
from collections import defaultdict, Counter

# TODO: online tf-idf cutoff by automatically cutting down large buckets over
# a given threshold. call it burst and erase already set counters


def jaccard_intersection_index(data, radius=0.8, key=None, min_size=2,
                               max_size=float('inf')):
    """
    Function returning an iterator over found clusters.

    It works by building an index of the given documents' tokens' intersection.

    It runs in subquadratic time: the less probable it is for two tokens to
    collide, the more it will approach linear time. As such, this algorithm
    is a good fit when handling large ngrams, for instance, but will be very
    poor when considering single characters as tokens since it means
    document will collide often because they will naturally share a lot of
    letters.

    As such, note that it would be possible to make this method faster by
    leveraging Zipf's law in some cases.

    Note also that this algorithm has perfect precision in that it does not
    try to approximate and will return the exact same result as a pairwise run.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        radius (number): Jaccard similarity radius.
        key (callable, optional): Function returning an item's key.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.

    Yield:
        list: A viable cluster.

    """
    buckets = defaultdict(list)
    intersections = defaultdict(Counter)

    if type(data) is not list:
        data = list(data)

    sizes = [0] * len(data)

    for i, item in enumerate(data):
        if key is not None:
            item = key(item)

        shingles = set(item)
        sizes[i] = len(shingles)

        for shingle in shingles:
            bucket = buckets[shingle]

            for j in bucket:
                intersections[i][j] += 1

            bucket.append(i)

    graph = defaultdict(list)

    for i, neighbors in intersections.items():

        for j, I in neighbors.items():
            U = sizes[i] + sizes[j] - I

            if I / U >= radius:
                graph[i].append(j)
                graph[j].append(i)

    visited = set()
    stack = []

    for i, neighbors in graph.items():
        if i in visited:
            continue

        visited.add(i)

        cluster = [data[i]]

        stack.extend(neighbors)

        while len(stack) != 0:
            j = stack.pop()

            if j in visited:
                continue

            cluster.append(data[j])
            visited.add(j)

            if j in graph:
                stack.extend(graph[j])

        yield cluster
