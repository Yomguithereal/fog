import csv
from timeit import default_timer as timer
from fog.clustering import minhash

with open('./data/musicians.csv', 'r') as f:
    reader = csv.DictReader(f)

    artists = set(line['artist'] for line in reader)

    print('%i artists' % len(artists))

    start = timer()

    clusters = list(minhash(artists, precision=1))
    print(timer() - start)

    for cluster in clusters:
        print(cluster)
