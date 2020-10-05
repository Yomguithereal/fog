import csv
import math
from collections import defaultdict, Counter
from fog.tokenizers import ngrams
from fog.clustering.ppjoin import ppjoin

with open('./data/universities.csv', 'r') as f:
    UNIVERSITIES = sorted(set([line['university'] for line in csv.DictReader(f)]))

CLUSTERS = [
    ['Kansas State University', 'Arkansas State University'],
    ['Taylor University', 'Baylor University'],
    ['La Salle University', 'De La Salle University'],
    ['Eastern Kentucky University', 'Western Kentucky University'],
    ['Eastern Michigan University', 'Western Michigan University'],
    ['Western Washington University', 'Eastern Washington University'],
    ['Iran University of Science and Technology', 'Jordan University of Science and Technology'],
    ['University of Western Australia', 'The University of Western Australia'],
    ['University of Western Ontario', 'The University of Western Ontario']
]

def tokenizer(x):
    return list(ngrams(5, x))

THRESHOLD = 0.8

result = list(ppjoin(UNIVERSITIES, THRESHOLD, tokenizer=tokenizer))

for pair in result:
    print(pair)

print(len(result), len(CLUSTERS))
