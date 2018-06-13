# =============================================================================
# Fog MinHash Clustering
# =============================================================================
#
# Clustering algorithm leveraging MinHash LSH to produce suitable clusters.
#
from collections import defaultdict
from fog.lsh.minhash import LSBMinHash


def minhash(data, precision=8):
    mh = LSBMinHash(precision=precision)

    buckets = defaultdict(list)

    for item in data:
        signature = mh.hash(item)

        for integer in signature:
            buckets[integer].append(item)

    for bucket in buckets.values():
        if len(bucket) > 1:
            yield bucket

    # TODO: merge buckets util
