import csv
import numpy as np
from random import sample
from experiments.utils import Timer
from fog.clustering import minhash, pairwise
from fog.metrics import jaccard_similarity
from fog.tokenizers import ngrams

def distinct_values(clusters):
    values = set()

    for cluster in clusters:
        values.update(cluster)

    return len(values)

def k_min_clusters(k, clusters):
    return sorted(clusters, key=lambda x: sorted(x)[0])[0:k]

with open('./data/universities.csv', 'r') as f:
    reader = csv.DictReader(f)

    universities = set(line['university'] for line in reader)

    TESTS = [.7, .8, .85]
    STATS = {}
    key = lambda x: list(ngrams(5, x))

    print('Universities: %i' % len(universities))
    print()

    print('Pairwise ground truth:')
    print('----------------------')
    for radius in TESTS:

        print('Radius: ', radius)
        with Timer():
            clusters = list(pairwise(universities, similarity=jaccard_similarity, radius=radius, key=key, mode='connected_components'))

        print('Distinct values:', distinct_values(clusters))
        print('Clusters:', len(clusters))
        print('Sample clusters:')
        for c in k_min_clusters(3, clusters):
            print('  ', c)
        print()

        STATS[radius] = distinct_values(clusters)

    print()

    print('MinHash')
    print('-------')
    for radius in TESTS:

        print('Radius: ', radius)
        with Timer():
            clusters = list(minhash(universities, radius=radius, key=key))

        print('Distinct values:', distinct_values(clusters))
        print('Clusters:', len(clusters))
        print('Precision:', distinct_values(clusters) / STATS[radius])
        print('Sample clusters:')
        for c in k_min_clusters(3, clusters):
            print('  ', c)
        print()
