import csv
from experiments.utils import Timer
from fog.clustering import minhash
from fog.tokenizers import ngrams

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

print('Artists:', len(artists))

key = lambda x: list(ngrams(5, x))
radius = 0.8

with Timer():
    clusters = list(minhash(artists, key=key, radius=radius))

for cluster in clusters:
    print(cluster)

print('Clusters:', len(clusters))
