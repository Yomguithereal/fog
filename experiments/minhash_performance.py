import csv
from experiments.utils import Timer
from fog.clustering import minhash, jaccard_intersection_index
from fog.tokenizers import ngrams

GROUND_TRUTH = 15

# ['Luna (singer)', 'Yuna (singer)']
# ['Lobo (musician)', 'Robo (musician)']
# ['Sam Jones (musician)', 'Adam Jones (musician)']
# ['Donnie Brooks', 'Lonnie Brooks']
# ['Dan Wilson (musician)', 'Alan Wilson (musician)', 'Ian Wilson (musician)']
# ['Arsenie Todiraş', 'Arsenie Todiraș']
# ['Tim Ward (musician)', 'Jim Ward (musician)']
# ['KK (singer)', 'K (singer)']
# ['Wando (singer)', 'Mando (singer)']
# ['Phillip Phillips', 'Flip Phillips']
# ['Mina (singer)', 'Dina (singer)']
# ['Nana (singer)', 'Bana (singer)', 'Jana (singer)']
# ['John Paris', 'John Parish']
# ['Ronnie Van Zant', 'Donnie Van Zant']
# ['Steve Nardelli', 'Steve Nardella']

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

print('Artists:', len(artists))

key = lambda x: list(ngrams(5, x))
radius = 0.8

print()
print('Minhash')
with Timer():
    clusters = list(minhash(artists, key=key, radius=radius, use_numpy=True))

for cluster in clusters:
    print(cluster)

print('Clusters:', len(clusters))
print('Precision:', len(clusters) / GROUND_TRUTH)

print()
print('Jaccard Intersection Index')
with Timer():
    clusters = list(jaccard_intersection_index(artists, key=key, radius=radius))

for cluster in clusters:
    print(cluster)

print('Clusters:', len(clusters))
print('Precision:', len(clusters) / GROUND_TRUTH)

