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

from fog.clustering.utils import clusters_from_buckets
from fog.lsh.minhash import MinHash
from fog.metrics.jaccard import jaccard_similarity


# TODO:
#   * Parallelize
#   * possibility to hash the band key
#   * note that we allow uneven bands for fine grained results
#   * double_check with minhash or jaccard or sub similarity even
#   * superminhash to generate signature faster (better for large docs)
#   * cheap_hashes
#   * possibility to use one dict per band + sum the integers

# TODO: compute similarities online + edge list -> connected components
# TODO: keep edge list in set of tuples with sorted comp not to compute
# n times the same similarity
# TODO: use pairs


def match_probability(h, bands, similarity):
    """
    Function returning the probability two pairs will match given a number
    of a signature's integers, the number of bands dividing the signature
    matrix and the desired similarity.

    Args:
        h (int): Number of integers in the minhash signature.
        bands (int): Number of bands dividing the signature matrix.
        similarity (float): Desired Jaccard similarity.

    Returns:
        float: The match probability.

    """
    return 1.0 - (1.0 - similarity ** (h / bands)) ** bands


def similarity_threshold(h, bands):
    """
    Function returning the Jaccard similarity threshold for minhash signature
    composed of h integers and a signature matrix divided in n bands.

    Args:
        h (int): Number of integers in the minhash signature.
        bands (int): Number of bands dividing the signature matrix.

    Returns:
        float: The Jaccard similarity threshold.

    """
    return (1.0 / bands) ** (1 / (h / bands))


def guess_bands(h, threshold):
    """
    Function used to iteratively guess the optimal number of bands needed to
    divide a minhash signature matrix in order to find pairs having a
    Jaccard similarity over the given threshold.

    Args:
        h (int): Number of integers in the minhash signature.
        threshold (float): Jaccard similarity threshold.

    Returns:
        int: The optimal number of bands.

    """

    bands = 1

    while bands <= h:
        t = similarity_threshold(h, bands)

        if t <= threshold:
            break

        bands += 1

    return bands


def minhash(data, h=256, key=None, radius=0.8, bands=None, use_numpy=False,
            seed=None):
    """
    Function returning an iterator over clusters found using the minhash
    clustering method.

    The idea is to compute minhash signatures for every item and divide the
    resulting signature matrix in bands of n rows so that if two items share
    the exact same rows in a band, they are likely to be similar.

    It runs in O(nh), n being the number of items, h the number of integers to
    use as minhash signature. Note that since usually h << n, it practically
    runs in O(n).

    Args:
        data (iterable): Items to cluster.
        h (int, optional): Number of integers to use as the minhash signature.
            Defaults to 256.
        key (callable, optional): Function returning an item's key.
        radius (float, optional): Radius over which a pair of items is deemed
            similar. Defaults to 0.8.
        bands (int, optional): By defaults, the function will attempt to guess
            the optimal number of bands to use to divide the signature matrix
            using given radius. Set this argument if you want to set the
            number of bands by yourself.
        use_numpy (bool, optional): whether to use numpy to speed up minhash
            signatures computations. Defaults to False.
        seed (int, optional): rng seed.

    """

    if bands is None:
        bands = guess_bands(h, radius)

    rows = h // bands
    h_upper_bound = bands * rows

    mh = MinHash(h, use_numpy=use_numpy, seed=seed)

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

    yield from clusters_from_buckets(
        buckets.values(),
        mode='connected_components',
        similarity=double_check
    )
