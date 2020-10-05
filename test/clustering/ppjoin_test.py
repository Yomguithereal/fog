# =============================================================================
# Fog PPJoin Clustering Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from fog.clustering import ppjoin
from fog.tokenizers import ngrams

with open('./data/universities.csv', 'r') as f:
    UNIVERSITIES = sorted(set([line['university'] for line in csv.DictReader(f)]))

JACCARD_5_GRAMS_T8_PAIRS = Clusters([
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

OVERLAP_5_GRAMS_T9_PAIRS = Clusters([
    ['American University', 'American University in Bulgaria'],
    ['BIMTECH', 'BIMTECH Bhubaneswar'],
    ['California State University%2C Channel Islands', 'California State University%2C Chico'],
    ['Concordia University', 'Concordia University (Quebec)'],
    ['Hamilton College', 'Hamilton College (New York)'],
    ['Hunter College', 'Hunter College, City University of New York'],
    ['Indiana University', 'Indiana University %E2%80%93 Purdue University Indianapolis'],
    ['Mindanao State University', 'Mindanao State University %E2%80%93 Iligan Institute of Technology'],
    ['Montana State University', 'Montana State University %E2%80%93 Bozeman'],
    ['Portland State University', 'Portland State University School of Business Administration'],
    ['Purdue University', 'Purdue University Calumet'],
    ['Rocky Mountain College', 'Rocky Mountain College      '],
    ['Santa Clara University', 'Santa Clara University College of Arts & Sciences'],
    ['Springfield College', 'Springfield College (Massachusetts)'],
    ['University of Alabama', 'University of Alabama at Birmingham'],
    ['University of Arkansas', 'University of Arkansas Honors College'],
    ['University of California', 'University of California%2C Berkeley'],
    ['University of Michigan', 'University of Michigan College of Engineering'],
    ['University of Milan', 'University of Milan    '],
    ['University of Missouri', 'University of Missouri College of Arts and Science'],
    ['University of Montana', 'University of Montana %E2%80%93 Missoula'],
    ['University of Saskatchewan', 'University of Saskatchewan College of Agriculture and Bioresources'],
    ['University of Tennessee', 'University of Tennessee at Chattanooga'],
    ['University of Toledo', 'University of Toledo Medical Center'],
    ['University of the Philippines', 'University of the Philippines Los Ba%C3%B1os'],
    ['Vanderbilt University', 'Vanderbilt University School of Engineering'],
    ['Washington & Jefferson College', 'Washington College'],
    ['Western Illinois University', 'Western Illinois University-Quad Cities']
])


# def naive_pairwise():
#     from fog.metrics import overlap_coefficient
#     from functools import partial

#     print()
#     key = partial(ngrams, 5)

#     for i in range(len(UNIVERSITIES)):
#         A  = key(UNIVERSITIES[i])

#         for j in range(i + 1, len(UNIVERSITIES)):
#             B = key(UNIVERSITIES[j])

#             if overlap_coefficient(A, B) >= 0.9:
#                 print([UNIVERSITIES[i], UNIVERSITIES[j]])

# naive_pairwise()


class TestPPJoin(object):
    def test_basics(self):
        pass
