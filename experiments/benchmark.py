import csv
from functools import partial
from timeit import default_timer as timer
from fog.clustering import *
from fog.metrics import jaccard_similarity
from fog.tokenizers import ngrams
from fog.key import fingerprint, omission_key, skeleton_key, damerau_levenshtein_1d_keys
from Levenshtein import distance as levenshtein
from cfog.metrics.levenshtein import limited_levenshtein_distance

with open('./data/universities.csv', 'r') as f:
    reader = csv.DictReader(f)

    universities = sorted(set(line['university'] for line in reader))

    print('Universities: %i' % len(universities))

    start = timer()
    clusters = list(pairwise_leader(universities, distance=levenshtein, radius=2))
    print('Leader (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(pairwise_fuzzy_clusters(universities, distance=levenshtein, radius=2))
    print('Fuzzy clusters (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(pairwise_connected_components(universities, distance=levenshtein, radius=2))
    print('Connected components (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(pairwise_connected_components(universities, distance=lambda x, y: limited_levenshtein_distance(2, x, y), radius=2))
    print('Limited Levenshtein connected components (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(vp_tree(universities, distance=levenshtein, radius=2))
    print('VPTree (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(quickjoin(universities, distance=levenshtein, radius=2))
    print('QuickJoin (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(nn_descent(universities, distance=levenshtein, radius=2))
    print('NN-Descent (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(nn_descent_full(universities, distance=levenshtein, radius=2))
    print('NN-Descent Full (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(blocking(universities, blocks=partial(ngrams, 6), distance=levenshtein, radius=2))
    print('Blocking (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(sorted_neighborhood(universities, key=omission_key, distance=levenshtein, radius=2))
    print('SNM Omission (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(sorted_neighborhood(universities, key=skeleton_key, distance=levenshtein, radius=2))
    print('SNM Skeleton (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(sorted_neighborhood(universities, keys=[omission_key, skeleton_key], distance=levenshtein, radius=2))
    print('SNM Omission + Skeleton (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(key_collision(universities, keys=damerau_levenshtein_1d_keys))
    print('Damerau-Levenshtein 1d (%i):' % len(clusters), timer() - start)

print()
with open('./data/musicians.csv', 'r') as f:
    reader = csv.DictReader(f)

    artists = sorted(set(line['artist'] for line in reader))

    print('Artists: %i' % len(artists))

    start = timer()
    clusters = list(key_collision(artists, keys=lambda x: ngrams(12, x), merge=True))
    print('12-grams key collision (%i)' % len(clusters), timer() - start)

    start = timer()
    clusters = list(key_collision(artists, key=fingerprint))
    print('Fingerprint key collision (%i)' % len(clusters), timer() - start)

    start = timer()
    clusters = list(key_collision(artists, keys=damerau_levenshtein_1d_keys))
    print('Damerau-Levenshtein 1d (%i)' % len(clusters), timer() - start)

    start = timer()
    clusters = list(blocking(artists, blocks=partial(ngrams, 6), distance=levenshtein, radius=2, processes=8))
    print('Blocking (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(sorted_neighborhood(artists, key=omission_key, distance=levenshtein, radius=2))
    print('SNM Omission (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(sorted_neighborhood(artists, key=skeleton_key, distance=levenshtein, radius=2))
    print('SNM Skeleton (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(sorted_neighborhood(artists, keys=[omission_key, skeleton_key], distance=levenshtein, radius=2))
    print('SNM Omission + Skeleton (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(quickjoin(artists, distance=levenshtein, radius=2, processes=8))
    print('QuickJoin (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(nn_descent(artists, distance=levenshtein, radius=2))
    print('NN-Descent (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(nn_descent_full(artists, distance=levenshtein, radius=2))
    print('NN-Descent Full (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(minhash(artists, radius=0.8, key=lambda x: list(ngrams(5, x)), use_numpy=True))
    print('MinHash (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(jaccard_intersection_index(artists, radius=0.8, key=lambda x: list(ngrams(5, x))))
    print('Jaccard Intersection Index (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(pairwise_fuzzy_clusters(artists, distance=levenshtein, radius=2, processes=8))
    print('Parallel Fuzzy clusters (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(pairwise_connected_components(artists, distance=levenshtein, radius=2, processes=8))
    print('Parallel connected components (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(pairwise_connected_components(artists, distance=lambda x, y: limited_levenshtein_distance(2, x, y), radius=2, processes=8))
    print('Parallel limited levenshtein connected components (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(vp_tree(artists, distance=levenshtein, radius=2))
    print('VPTree clusters (%i)' % len(clusters), timer() - start)
