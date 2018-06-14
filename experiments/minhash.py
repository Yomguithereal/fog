import csv
from timeit import default_timer as timer
from fog.clustering import minhash
from fog.metrics import jaccard_similarity
from fog.tokenizers import ngrams

with open('./data/musicians.csv', 'r') as f:
    reader = csv.DictReader(f)

    artists = set(line['artist'] for line in reader)

    print('%i artists' % len(artists))

    key = lambda x: x

    start = timer()

    clusters = list(minhash(artists, key=key))
    print('MinHash (%i)' % len(clusters), timer() - start)

    for cluster in clusters:
        print(cluster, jaccard_similarity(key(cluster[0]), key(cluster[1])))
