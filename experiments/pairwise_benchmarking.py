import csv
from timeit import default_timer as timer
from fog.clustering import *
from Levenshtein import distance as levenshtein

with open('./data/musicians.csv', 'r') as f:
    reader = csv.DictReader(f)

    artists = set(line['artist'] for line in reader)

    for cluster in pairwise_fuzzy_clusters(artists, distance=levenshtein, radius=2):
        print(cluster)
