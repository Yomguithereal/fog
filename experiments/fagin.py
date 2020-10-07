import csv
import pytest
from collections import Counter
from fog.clustering.fagin import fagin_k1, threshold_algorithm_k1, naive_cosine_pairs
from fog.tokenizers import ngrams
from fog.metrics import sparse_cosine_similarity
from experiments.utils import Timer

with open('./data/universities.csv', 'r') as f:
    UNIVERSITIES = sorted(set([line['university'] for line in csv.DictReader(f)]))

with open('./data/fagin_k1_ground_truth.csv') as f:
    GROUND_TRUTH = {int(row[0]): (int(row[1]), float(row[2])) for row in csv.reader(f)}

VECTORS = [Counter(ngrams(2, chars)) for chars in UNIVERSITIES]

with Timer('quadratic'):
    # with open('./data/fagin_k1_ground_truth.csv', 'w') as f:
    # writer = csv.writer(f)

    for i in range(len(VECTORS)):
        v1 = VECTORS[i]
        best = None

        for j in range(len(VECTORS)):
            if i == j:
                continue

            v2 = VECTORS[j]

            c = sparse_cosine_similarity(v1, v2)

            # NOTE: this is stable and lower index wins
            if best is None or c > best[0]:
                best = (c, j)

        # print(UNIVERSITIES[i], UNIVERSITIES[best[1]])
        # writer.writerow([i, best[1], str(best[0])])

with Timer('FA'):
    for i, candidates in fagin_k1(VECTORS):
        v = VECTORS[i]
        j = max(candidates, key=lambda c: sparse_cosine_similarity(v, VECTORS[c]))

        # print("'%s'" % UNIVERSITIES[i])
        # print("'%s'" % UNIVERSITIES[GROUND_TRUTH[i][0]])
        # print("'%s'" % UNIVERSITIES[j])
        # print(i, j, len(candidates), GROUND_TRUTH[i], sparse_cosine_similarity(v, VECTORS[j]))

        assert j == GROUND_TRUTH[i][0]

with Timer('TA'):

    # TODO: current heap comparison used is not stable
    for i, j in threshold_algorithm_k1(VECTORS):
        if i != j:
            assert sparse_cosine_similarity(VECTORS[i], VECTORS[j]) == pytest.approx(GROUND_TRUTH[i][1])

with Timer('naive cosine pairs'):
    pairs = list(naive_cosine_pairs(VECTORS))
    n = len(VECTORS) * (len(VECTORS) - 1) // 2

    print(len(pairs), n, len(pairs) / n)
