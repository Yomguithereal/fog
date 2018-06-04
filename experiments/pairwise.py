import csv
from fog.clustering import leader, pairwise, fuzzy_pairwise
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

    print('Pairwise')
    for cluster in pairwise(publishers, distance=levenshtein, radius=2):
      print(cluster)

    print()
    print('Pairwise fuzzy')
    for cluster in fuzzy_pairwise(publishers, distance=levenshtein, radius=2):
        print(cluster)

    print()
    print('Leader')
    for cluster in leader(publishers, distance=levenshtein, radius=2):
      print(cluster)
