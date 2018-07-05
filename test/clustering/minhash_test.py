# =============================================================================
# Fog MinHash Clustering Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from fog.clustering import minhash
from fog.tokenizers import ngrams

with open('./data/universities.csv', 'r') as f:
    UNIVERSITIES = set([line['university'] for line in csv.DictReader(f)])

CLUSTERS = Clusters([
    ['Kansas State University', 'Arkansas State University'],
    ['Taylor University', 'Baylor University'],
    ['La Salle University', 'De La Salle University'],
    ['Eastern Kentucky University', 'Western Kentucky University'],
    ['Eastern Michigan University', 'Western Michigan University'],
    ['Western Washington University', 'Eastern Washington University'],
    ['Iran University of Science and Technology', 'Jordan University of Science and Technology'],
    ['University of Western Australia', 'The University of Western Australia'],
    ['University of Western Ontario', 'The University of Western Ontario']
])


class TestMinHash(object):
    def test_basics(self):
        def key(x):
            return list(ngrams(5, x))

        clusters = Clusters(minhash(UNIVERSITIES, key=key, radius=0.8, seed=123))

        assert clusters == CLUSTERS
