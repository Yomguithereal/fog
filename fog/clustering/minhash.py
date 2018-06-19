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


# TODO: optimize probability iteratively to find number of bands
# Note than ideally, number of rows should divide 64 evenly
# TODO: else try also to find precision
# TODO: step 1 bands option + sane iteration + experiments with threshold to see what gives

# TODO: parallelize

def match_probability(h, bands, similarity):
    return 1.0 - (1.0 - similarity ** (h / bands)) ** bands


def similarity_threshold(h, bands):
    return (1.0 / bands) ** (1 / (h / bands))


def guess_bands(precision, radius, probability):
    h = precision * 64

    bands = 1

    while bands <= h:
        p = match_probability(h, bands, radius)

        if p >= probability:
            break

        bands += 1

        while h % bands != 0:
            bands += 1

    return bands

# TODO: double_check with jaccard or minhash, sub similarity or true radius
# TODO: compute on 64 * precision to avoid modulo issues and filtering out
# TODO: need to think in bands ^ not bands = precision
# TODO: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4431368/
# TODO: superminhash https://arxiv.org/pdf/1706.05698.pdf
# TODO: faster hashing https://stackoverflow.com/questions/19701052/how-many-hash-functions-are-required-in-a-minhash-algorithm


def minhash(data, precision=4, key=None, radius=0.8, probability=0.9):

    h = precision * 64

    # NOTE: it seems we need to divide the bands by 2 because of LSB
    bands = max(1, guess_bands(precision, radius, probability) // 2)
    rows = h // bands

    mh = LSBMinHash(precision=precision)

    buckets = defaultdict(list)

    for item in data:
        k = item

        if key is not None:
            k = key(item)

        signature = mh.hash(k)

        binary = ''.join([bin(i)[2:].rjust(64, '0') for i in signature])

        for band in range(0, h, rows):
            band_key = (band, binary[band:band + rows])
            buckets[band_key].append(item)

    yield from merge_buckets_into_clusters(buckets.values(), mode='connected_components')
