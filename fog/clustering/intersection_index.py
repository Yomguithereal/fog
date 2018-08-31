# =============================================================================
# Fog Key Intersection Clustering
# =============================================================================
#
# Clustering routine leveraging an intersection index to find similar items.
#
from collections import defaultdict, Counter
from fog.clustering.utils import clusters_from_pairs

# TODO: online tf-idf cutoff by automatically cutting down large buckets over
# a given threshold. call it burst and erase already set counters

# TODO: cosine variants

# NOTE: compromise between key collision & meta blocking

# TODO: found in the litterature as pair-count / probe count
# ref in sarawagi-kirpal

METRICS = ['jaccard', 'overlap']


def intersection_index(data, metric='jaccard', radius=0.8, key=None, min_size=2,
                       max_size=float('inf'), mode='connected_components'):
    """
    Function returning an iterator over found clusters.

    It works by building an index of the given documents' tokens' intersection.

    It runs in subquadratic time: the less probable it is for two tokens to
    collide, the more it will approach linear time. As such, this algorithm
    is a good fit when handling large ngrams, for instance, but will be very
    poor when considering single characters as tokens since it means
    document will collide often because they will naturally share a lot of
    letters.

    As such, note that it is possible to make this method faster by leveraging
    Zipf's law in some cases.

    Note also that this algorithm is on par with pairwise methods in that it
    does not try to approximate and will return all the existing pairs.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        metric (string, optional): Metric to use. One of {'jaccard', 'overlap'}.
            Defaults to 'jaccard'.
        radius (number, optional): Jaccard similarity radius.
        key (callable, optional): Function returning an item's key.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.

    Yield:
        list: A viable cluster.

    """

    if metric not in METRICS:
        raise TypeError('fog.clustering.intersection_index: unknown metric "%s"' % metric)

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

    def clustering():
        for i, neighbors in intersections.items():

            for j, I in neighbors.items():

                if metric == 'jaccard':
                    U = sizes[i] + sizes[j] - I

                    if I / U >= radius:
                        yield (i, j)

                else:
                    M = min(sizes[i], sizes[j])

                    if I / M >= radius:
                        yield (i, j)

    gen = clusters_from_pairs(
        clustering(),
        min_size=min_size,
        max_size=max_size,
        mode=mode
    )

    for cluster in gen:
        yield [data[i] for i in cluster]
