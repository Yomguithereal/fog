import csv
from timeit import default_timer as timer
from fog.clustering import *
from Levenshtein import distance as levenshtein

with open('./data/musicians.csv', 'r') as f:
    reader = csv.DictReader(f)

    artists = set(line['artist'] for line in reader)

    for cluster in key_collision(artists, key=lambda x: ' '.join(sorted(set(x.strip().lower().split(' '))))):
        print(cluster)
