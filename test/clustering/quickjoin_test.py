# =============================================================================
# Fog QuickJoin Clustering Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from Levenshtein import distance as levenshtein
from fog.clustering import quickjoin
from fog.metrics import jaccard_similarity

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


class TestQuickJoin(object):
    def test_basics(self):
        clusters = Clusters(quickjoin(DATA, distance=levenshtein, radius=1))

        assert clusters == CLUSTERS

        sim_clusters = Clusters(quickjoin(DATA, similarity=jaccard_similarity, radius=0.8))

        assert clusters == CLUSTERS

    def test_universities(self):
        clusters = Clusters(quickjoin(UNIVERSITIES, distance=levenshtein, radius=1))

        assert clusters == UNIVERSITY_CLUSTERS

        parallel_clusters = Clusters(quickjoin(UNIVERSITIES, distance=levenshtein, radius=1, processes=2))

        assert parallel_clusters == UNIVERSITY_CLUSTERS

        vptree_clusters = Clusters(quickjoin(UNIVERSITIES, distance=levenshtein, radius=1))

        assert vptree_clusters == UNIVERSITY_CLUSTERS
