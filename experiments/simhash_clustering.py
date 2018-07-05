import csv
import math
import sys
import itertools
import numpy as np
from fog.lsh import simhash, simhash_similarity
from fog.metrics import cosine_similarity
from fog.tokenizers import ngrams
from fog.clustering.utils import merge_buckets_into_clusters
from collections import defaultdict, Counter
from progressbar import ProgressBar

GROUND_TRUTH = 132

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

buckets = defaultdict(list)

f = 64
radius = 0.8
key = lambda x: list(ngrams(5, x))
sh = lambda x: simhash(key(x), f=f)
k = math.floor((1.0 - radius) * f)

print('f', f)
print('k', k)

# NOTE: does not work -> need to rotate the bits
# https://github.com/leonsim/simhash/blob/master/simhash/__init__.py#L116-L208
# https://github.com/scrapinghub/python-simhash
# http://www.wwwconference.org/www2007/papers/paper215.pdf
# https://github.com/seomoz/simhash-cpp/tree/e7aacb1642f406ff0815cf402e909d2002473812
# https://ir.library.dc-uoit.ca/bitstream/10155/475/1/Rodriguez%20Reina_Ernesto.pdf
# Guessing b, should be smallest power of 2 greater than k
b = 2

while b < k:
    b *= 2

b = 6

r = f // b

t = b - k

print('b', b)
print('r', r)
print('t', t)

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


def minhash(data, h=128, key=None, radius=0.8, bands=None, use_numpy=False):
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

    """

    if bands is None:
        bands = guess_bands(h, radius)
    print(bands)
    rows = h // bands
    h_upper_bound = bands * rows

    buckets = defaultdict(list)

    bar = ProgressBar()
    for item in bar(data):
        k = item

        if key is not None:
            k = key(item)

        signature = simhash(k, 128)
        binary = bin(signature)[2:].rjust(f, '0')

        for band in range(0, h_upper_bound, rows):
            band_key = (band, binary[band:band + rows])
            buckets[band_key].append(item)

    def double_check(A, B):
        if key is not None:
            return cosine_similarity(key(A), key(B)) >= radius

        return cosine_similarity(A, B) >= radius

    yield from merge_buckets_into_clusters(
        buckets.values(),
        mode='connected_components',
        similarity=double_check
    )

clusters = list(minhash(artists, key=key, radius=radius))

print(len(clusters))

# print('Buckets...')
# bar = ProgressBar()
# for artist in bar(sorted(artists)):
#     binary = bin(sh(artist))[2:].rjust(f, '0')

#     for i, band in enumerate(range(0, 64, 16)):
#         kk = (i, binary[band:band + 16])
#         buckets[kk].append(artist)

# print(len(buckets))
# print(np.median(np.fromiter((len(b) for b in buckets.values()), int)))
# print(min(len(b) for b in buckets.values()), max(len(b) for b in buckets.values()))
# print(sum(1 for b in buckets.values() if len(b) > 1))

# graph = defaultdict(set)

# for bucket in buckets.values():
#     if len(bucket) < 2:
#         continue

#     for i, item1 in enumerate(bucket):
#         for j, item2 in enumerate(bucket):
#             if (item2 in graph and item1 in graph[item2]) or (item1 in graph and item2 in graph[item1]):
#                 continue

#             if cosine_similarity(key(item1), key(item2)) >= radius:
#                 graph[item1].add(item2)
#                 graph[item2].add(item1)

# visited = set()
# stack = []

# for item, neighbors in graph.items():
#     if item in visited:
#         continue

#     visited.add(item)

#     cluster = [item]

#     stack.extend(neighbors)

#     while len(stack) != 0:
#         neighbor = stack.pop()

#         if neighbor in visited:
#             continue

#         cluster.append(neighbor)
#         visited.add(neighbor)

#         stack.extend(graph[neighbor])

#     if len(cluster) >= 2:
#         print(cluster)

# for b in buckets.values():
#     if len(b) > 1:
#         print(b)
#         print()
# clusters = list(merge_buckets_into_clusters(buckets.values(), similarity=lambda x, y: cosine_similarity(key(x), key(y)) >= 0.8))

# print('Clusters', clusters_count, '/', GROUND_TRUTH)
# print('Precision', clusters_count / GROUND_TRUTH)
# print('Candidates', candidates, '/', int(len(artists) * (len(artists) - 1) / 2))
# print('Ratio', candidates / int(len(artists) * (len(artists) - 1) / 2))
