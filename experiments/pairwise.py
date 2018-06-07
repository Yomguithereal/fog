from fog.clustering import *
from fog.metrics import jaccard_similarity
from Levenshtein import distance as levenshtein

data = [
  'abc',
  'bcd',
  'cde',
  'def',
  'efg',
  'fgh',
  'ghi'
]

print('Pairwise leader')
for cluster in pairwise(data, distance=levenshtein, radius=2):
  print(cluster)

print()
print('Pairwise fuzzy')
for cluster in pairwise_fuzzy_clusters(data, distance=levenshtein, radius=2):
    print(cluster)

print()
print('Pairwise connected components')
for cluster in pairwise_connected_components(data, distance=levenshtein, radius=2):
  print(cluster)

print()
print('VPTree')
for cluster in vp_tree(data, distance=levenshtein, radius=2):
  print(cluster)
