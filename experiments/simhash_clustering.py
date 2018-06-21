import csv
from fog.lsh import simhash, simhash_similarity
from fog.metrics import sparse_cosine_similarity
from fog.tokenizers import ngrams
from collections import defaultdict, Counter

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

buckets = defaultdict(list)
graph = defaultdict(Counter)

sh = lambda x: simhash(ngrams(5, x))

for university in artists:
    h = bin(sh(university))[2:]

    radius = 0.8

    # k = floor((1.0 - radius) * 128)

    k = 25

    # TODO: find equation to optimize r & m
    # TODO: what if k does not divide 128
    # TODO: try a 64 bits version also with f parameter
    r = 16
    m = 128 // r

    for i in range(0, 128, r):
        key = (i, h[i:i + r])

        bucket = buckets[key]

        for neighbor in bucket:
            graph[university][neighbor] += 1
            graph[neighbor][university] += 1

        bucket.append(university)

candidates = 0

visited = set()
for university, neighbors in graph.items():
    if university in visited:
        continue

    cluster = [university]

    for neighbor, count in neighbors.items():
        if count > m - k:
            candidates += 1

            if sparse_cosine_similarity(Counter(ngrams(5, university)), Counter(ngrams(5, neighbor))) >= radius:
                cluster.append(neighbor)

    visited.update(cluster)

    if len(cluster) > 1:
        print(cluster)

print('Candidates', candidates, '/', int(len(artists) * (len(artists) - 1) / 2))
