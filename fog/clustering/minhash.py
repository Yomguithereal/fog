# =============================================================================
# Fog MinHash Clustering
# =============================================================================
#
# Clustering algorithm leveraging MinHash LSH to produce suitable clusters.
#
from collections import defaultdict

from fog.clustering.utils import merge_buckets_into_clusters
from fog.lsh.minhash import LSBMinHash


def minhash(data, precision=4, key=None, rows=1):

    N = precision * 64
    assert N % rows == 0
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
