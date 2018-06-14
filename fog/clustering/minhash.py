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
from fog.lsh.minhash import LSBMinHash


def needed_rows_for_threshold(precision, threshold):
    d = 1.0 - threshold

    r = math.log(1.0 / precision) / math.log(d)

    return math.ceil(r)


# TODO: double_check with jaccard or minhash, sub similarity or true radius


def minhash(data, precision=4, key=None, threshold=0.6):

    rows = needed_rows_for_threshold(precision, threshold)
    bands = 64 // rows

    mh = LSBMinHash(precision=precision)

    buckets = defaultdict(list)

    for item in data:
        k = item

        if key is not None:
            k = key(item)

        signature = mh.hash(k)

        for integer in signature:
            binary = bin(integer)[2:].rjust(64, '0')

            i = 0
            for row in range(0, 64, bands):
                band = '%i§%s' % (i, binary[row:row + bands])

                buckets[band].append(item)
                i += 1

    yield from merge_buckets_into_clusters(buckets.values())
