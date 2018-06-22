import csv
import math
from fog.lsh import simhash, simhash_similarity
from fog.metrics import cosine_similarity
from fog.tokenizers import ngrams
from collections import defaultdict, Counter
from progressbar import ProgressBar

GROUND_TRUTH = 132

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

buckets = defaultdict(list)
graph = defaultdict(Counter)

f = 128
radius = 0.8
sh = lambda x: simhash(ngrams(5, x), f=f)
k = math.floor((1.0 - radius) * f)

print('f', f)
print('k', k)

# NOTE: does not work -> need to rotate the bits
# https://github.com/leonsim/simhash/blob/master/simhash/__init__.py#L116-L208

# Guessing b, should be smallest power of 2 greater than k
b = 2

while b < k:
    b *= 2

b = 16

r = f // b

t = b - k

print('b', b)
print('r', r)
print('t', t)

print('Buckets...')
bar = ProgressBar()
for artist in bar(artists):

    # TODO: don't need to get bin since we can slice the number's bits
    h = bin(sh(artist))[2:]

    for i in range(0, f, r):
        key = (i, h[i:i + r])

        bucket = buckets[key]

        for neighbor in bucket:
            graph[artist][neighbor] += 1
            graph[neighbor][artist] += 1

        bucket.append(artist)

print('Merging...')
candidates = 0
clusters_count = 0
visited = set()
for artist, neighbors in graph.items():
    if artist in visited:
        continue

    cluster = [artist]

    for neighbor, count in neighbors.items():
        if count > t:
            candidates += 1

            if cosine_similarity(ngrams(5, artist), ngrams(5, neighbor)) >= radius:
                cluster.append(neighbor)

    visited.update(cluster)

    if len(cluster) > 1:
        clusters_count += 1
        print(cluster)

print('Clusters', clusters_count, '/', GROUND_TRUTH)
print('Precision', clusters_count / GROUND_TRUTH)
print('Candidates', candidates, '/', int(len(artists) * (len(artists) - 1) / 2))
print('Ratio', candidates / int(len(artists) * (len(artists) - 1) / 2))
