import csv
from functools import partial
from timeit import default_timer as timer
from fog.clustering import *
from fog.tokenizers import ngrams
from fog.key import fingerprint, omission_key
from Levenshtein import distance as levenshtein

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
    clusters = list(vp_tree(universities, distance=levenshtein, radius=2))
    print('VPTree (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(blocking(universities, blocks=partial(ngrams, 6), distance=levenshtein, radius=2))
    print('Blocking (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(sorted_neighborhood(universities, key=omission_key, distance=levenshtein, radius=2))
    print('SNM Omission (%i):' % len(clusters), timer() - start)

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
    clusters = list(blocking(artists, blocks=partial(ngrams, 6), distance=levenshtein, radius=2, processes=8))
    print('Blocking (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(sorted_neighborhood(artists, key=omission_key, distance=levenshtein, radius=2))
    print('SNM Omission (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(pairwise_fuzzy_clusters(artists, distance=levenshtein, radius=2, processes=8))
    print('Parallel Fuzzy clusters (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(pairwise_connected_components(artists, distance=levenshtein, radius=2, processes=8))
    print('Parallel connected components (%i):' % len(clusters), timer() - start)

    start = timer()
    clusters = list(vp_tree(artists, distance=levenshtein, radius=2))
    print('VPTree clusters (%i)' % len(clusters), timer() - start)
