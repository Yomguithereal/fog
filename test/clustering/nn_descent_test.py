# =============================================================================
# Fog NN-Descent Clustering Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from Levenshtein import distance as levenshtein
from fog.clustering import nn_descent

DATA = [
    'Mister Hyde',
    'Mister Hide',
    'Claudia Loc',
    'Cladia Loc'
]

CLUSTERS = Clusters([
    ('Mister Hyde', 'Mister Hide'),
    ('Claudia Loc', 'Cladia Loc')
])

UNIVERSITY_CLUSTERS = Clusters([
    ('Universidad De Manila', 'Universidad de Manila'),
    ('DePaul University', 'DePauw University'),
    ('Seton Hall University', 'Seton Hill University'),
    ('Baylor University', 'Taylor University')
])

with open('./data/universities.csv', 'r') as f:
    UNIVERSITIES = set([line['university'] for line in csv.DictReader(f)])


class TestNNDescent(object):
    def test_basics(self):
        clusters = Clusters(nn_descent(DATA, k=1, distance=levenshtein, radius=1, seed=123))

        assert clusters == CLUSTERS

    def test_universities(self):
        clusters = Clusters(nn_descent(UNIVERSITIES, distance=levenshtein, radius=1, seed=123))

        assert clusters == UNIVERSITY_CLUSTERS

        parallel_clusters = Clusters(nn_descent(UNIVERSITIES, distance=levenshtein, radius=1, seed=123))

        assert parallel_clusters == UNIVERSITY_CLUSTERS
