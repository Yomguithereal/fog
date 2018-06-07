import csv
from timeit import default_timer as timer
from fog.clustering import *
from Levenshtein import distance as levenshtein

# with open('./data/universities.csv', 'r') as f:
#     reader = csv.DictReader(f)

#     universities = sorted(set(line['university'] for line in reader))

#     print('Universities: %i' % len(universities))

#     start = timer()
#     clusters = list(pairwise_leader(universities, distance=levenshtein, radius=2))
#     print('Leader (%i):' % len(clusters), timer() - start)

#     start = timer()
#     clusters = list(pairwise_fuzzy_clusters(universities, distance=levenshtein, radius=2, processes=2))
#     print('Fuzzy clusters (%i):' % len(clusters), timer() - start)

#     start = timer()
#     clusters = list(pairwise_connected_components(universities, distance=levenshtein, radius=2))
#     print('Connected components (%i):' % len(clusters), timer() - start)

with open('./data/musicians.csv', 'r') as f:
    reader = csv.DictReader(f)

    artists = sorted(set(line['artist'] for line in reader))

    print('Artists: %i' % len(artists))

    start = timer()
    clusters = list(pairwise_fuzzy_clusters(artists, distance=levenshtein, radius=2, processes=6))
    print('Fuzzy clusters (%i):' % len(clusters), timer() - start)
