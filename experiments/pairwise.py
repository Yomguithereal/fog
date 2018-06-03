import csv
from fog.clustering import pairwise
from fog.metrics import jaccard_similarity
from Levenshtein import distance as levenshtein

with open('./data/figshare.csv', 'r') as f:
    reader = csv.DictReader(f)

    publishers = set([line['Publisher'] for line in reader])

    publishers = [
      'abc',
      'bcd',
      'cde',
      'def',
      'efg',
      'fgh',
      'ghi'
    ]

    for cluster in pairwise(publishers, distance=levenshtein, radius=2, fuzzy_clusters=True):
        print(cluster)
