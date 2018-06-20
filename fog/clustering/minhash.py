# =============================================================================
# Fog MinHash Clustering
# =============================================================================
#
# Clustering algorithm leveraging MinHash LSH to produce suitable clusters.
#
# [Url]:
# http://infolab.stanford.edu/~ullman/mmds/ch3.pdf
#
from collections import defaultdict
import math

from fog.clustering.utils import merge_buckets_into_clusters
from fog.lsh.minhash import LSBMinHash, MinHash
from fog.metrics.jaccard import jaccard_similarity


# TODO:
#   * Parallelize
#   * possibility to hash the band key
#   * note that we allow uneven bands for fine grained results
#   * double_check with minhash or jaccard or sub similarity even
#   * superminhash to generate signature faster
#   * cheap_hashes
#   * docs
#   * possibility to use one dict per band + sum the integers


def match_probability(h, bands, similarity):
    return 1.0 - (1.0 - similarity ** (h / bands)) ** bands


def similarity_threshold(h, bands):
    return (1.0 / bands) ** (1 / (h / bands))


def guess_bands(h, threshold):
    bands = 1

    while bands <= h:
        t = similarity_threshold(h, bands)

        if t <= threshold:
            break

        bands += 1

    return bands


def minhash(data, h=256, key=None, radius=0.8, bands=None):

    if bands is None:
        bands = guess_bands(h, radius)

    rows = h // bands
    h_upper_bound = bands * rows

    mh = MinHash(h)

    buckets = defaultdict(list)

    for item in data:
        k = item

        if key is not None:
            k = key(item)

        signature = mh.create_signature(k)

        for band in range(0, h_upper_bound, rows):
            band_key = (band, '%'.join(str(n) for n in signature[band:band + rows]))
            buckets[band_key].append(item)

    def double_check(A, B):
        if key is not None:
            return jaccard_similarity(key(A), key(B)) >= radius

        return jaccard_similarity(A, B) >= radius

    yield from merge_buckets_into_clusters(
        buckets.values(),
        mode='connected_components',
        similarity=double_check
    )
