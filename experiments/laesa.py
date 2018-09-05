import csv
from experiments.utils import Timer
from fog.clustering import laesa
from Levenshtein import distance as levenshtein

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

print(len(artists))

with Timer('LAESA'):
    clusters = list(laesa(artists, distance=levenshtein, radius=1))

for cluster in clusters:
    print(cluster)

NB_CLUSTERS = 138
print('Recall %f' % (len(clusters) / NB_CLUSTERS))
