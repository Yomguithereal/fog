import csv
from fog.key import levenshtein_1d
from Levenshtein import distance as levenshtein
from fog.clustering import key_collision, pairwise

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

print(len(artists))

pairwise_clusters = list(pairwise(artists, distance=levenshtein, radius=1, processes=8))
key_clusters = list(key_collision(artists, keys=levenshtein_1d))

print(len(pairwise_clusters) == len(key_clusters))

A = set()
B = set()

for c in pairwise_clusters:
    A.update(c)

for c in key_clusters:
    B.update(c)

print(A == B)
