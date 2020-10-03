import csv
import math
from collections import defaultdict, Counter
from fog.tokenizers import ngrams

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

def key(x):
    return list(ngrams(5, x))

THRESHOLD = 0.8

UNIVERSITIES_NGRAMS = sorted([key(u) for u in UNIVERSITIES], key=len)

# TODO: it's probably more useful to transform into integer tokens
# NOTE: it's useless if you keep alphabetical order by the way
def infer_order(records):
    tokens = set()

    for item in records:
        for x in item:
            tokens.add(x)

    return {token: i for i, token in enumerate(sorted(tokens))}


def prefix_length(record, threshold):
    return min(len(record) - math.ceil(threshold * len(record)) + 1, len(record))


def overlap_constraint(l1, l2, threshold):
    return math.ceil(threshold / (1.0 + threshold) * (l1 + l2))


# TODO: need to chose a way to sort tokens according to random or frequency
def ppjoin(records, threshold):
    index = defaultdict(set)
    candidates = set()

    records = [sorted(record) for record in records]
    order_map = infer_order(records)

    for record_index, record in enumerate(records):

        # If record is empty
        if not record:
            continue

        xp = prefix_length(record, threshold)
        overlaps = Counter()

        for i in range(xp):
            item = record[i]

            # TODO: optimize
            for other_index, j in index.get(item, []):
                other = records[other_index]

                if len(other) < threshold * len(record):
                    continue

                alpha = overlap_constraint(len(record), len(other), threshold)
                upper_bound = 1 + min(len(record) - i, len(other) - j)

                if overlaps.get(other_index, 0) + upper_bound >= alpha:
                    overlaps[other_index] += 1
                else:
                    overlaps[other_index] = 0 # Looks like a delete

            index[item].add((record_index, i))

        # Suffixes
        for other_index, overlap in overlaps.items():
            other = records[other_index]

            yp = prefix_length(other, threshold)

            wx = record[xp - 1]
            wy = other[yp - 1]
            alpha = overlap_constraint(len(record), len(other), threshold)
            rest = 0

            if order_map[wx] < order_map[wy]:
                ubound = overlap + len(record) - xp

                # TODO: optimize intersection count
                if ubound >= alpha:
                    rest = len(set(other[overlap:]) & set(record[xp:]))
            else:
                ubound = overlap + len(other) - yp

                if ubound >= alpha:
                    rest = len(set(record[overlap:]) & set(other[yp:]))

            overlap += rest

            if overlap >= alpha:

                # TODO: check how often candidates are repeated
                candidates.add((record_index, other_index))

    return [(records[i], records[j]) for i, j in candidates]

result = ppjoin(UNIVERSITIES_NGRAMS, THRESHOLD)

for pair in result:
    print(pair)

print(len(result), len(CLUSTERS))
