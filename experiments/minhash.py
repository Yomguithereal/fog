import csv
import numpy as np
from timeit import default_timer as timer
from fog.clustering import minhash, pairwise
from fog.metrics import jaccard_similarity
from fog.tokenizers import ngrams

def distinct_values(clusters):
    values = set()

    for cluster in clusters:
        values.update(cluster)

    return len(values)

# with open('./data/musicians.csv', 'r') as f:
#     reader = csv.DictReader(f)

#     artists = set(line['artist'] for line in reader)

#     print('%i artists' % len(artists))

#     key = lambda x: ngrams(3, x)

#     start = timer()

#     clusters = list(minhash(artists, key=key))
#     time = timer() - start

#     ds = []
#     for cluster in clusters:
#         d = jaccard_similarity(key(cluster[0]), key(cluster[1]))
#         print(cluster, d)
#         ds.append(d)

#     print('Time', time)
#     if len(clusters):
#         print('Median', np.median(ds))
#         print('Min', min(ds))
#     print('Clusters', len(clusters))

    # clusters = list(pairwise((list(key(a)) for a in artists), processes=8, similarity=jaccard_similarity, radius=0.6))

    # for cluster in clusters:
    #     print(cluster)

    # print(len(clusters))

with open('./data/universities.csv', 'r') as f:
    reader = csv.DictReader(f)

    universities = set(line['university'] for line in reader)

    print('%i universities' % len(universities))

    clusters = list(minhash(universities, precision=4, threshold=0.9))

    # for cluster in clusters:
    #     print(cluster)

    # TODO: Compare found items, use ngrams also
    print(distinct_values(clusters))

    clusters = list(pairwise(universities, mode='connected_components', similarity=jaccard_similarity, radius=0.9))

    print(distinct_values(clusters))

    # for cluster in clusters:
    #     print(cluster)
