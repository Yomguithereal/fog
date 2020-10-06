# =============================================================================
# Fog PPJoin Clustering Unit Tests
# =============================================================================
import csv
from test.clustering.utils import Clusters
from fog.clustering import ppjoin
from fog.tokenizers import ngrams
from fog.metrics import (
    jaccard_similarity,
    dice_coefficient,
    binary_cosine_similarity
)


def tokenizer(r):
    return ngrams(5, r)


with open('./data/universities.csv', 'r') as f:
    UNIVERSITIES = sorted(set([line['university'] for line in csv.DictReader(f)]))

CLUSTERINGS = [
    {},
    {'allpairs': True},
    {'plus': True}
]

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

DICE_5_GRAMS_T85_PAIRS = Clusters([
    ['Arkansas State University', 'Kansas State University'],
    ['Aston University', 'Boston University'],
    ['Baylor University', 'Taylor University'],
    ['De La Salle University', 'La Salle University'],
    ['Eastern Kentucky University', 'Western Kentucky University'],
    ['Eastern Michigan University', 'Western Michigan University'],
    ['Eastern Washington University', 'Western Washington University'],
    ['Iran University of Science and Technology', 'Jordan University of Science and Technology'],
    ['Iran University of Science and Technology', 'Pohang University of Science and Technology'],
    ['Ohio Wesleyan University', 'Wesleyan University'],
    ['Rocky Mountain College', 'Rocky Mountain College      '],
    ['Southern Connecticut State University', 'Western Connecticut State University'],
    ['The University of Western Australia', 'University of Western Australia'],
    ['The University of Western Ontario', 'University of Western Ontario'],
    ['University of Milan', 'University of Milan    ']
])

BINARY_COSINE_5_GRAMS_T9_PAIRS = Clusters([
    ['Arkansas State University', 'Kansas State University'],
    ['Baylor University', 'Taylor University'],
    ['De La Salle University', 'La Salle University'],
    ['Eastern Kentucky University', 'Western Kentucky University'],
    ['Eastern Michigan University', 'Western Michigan University'],
    ['Eastern Washington University', 'Western Washington University'],
    ['Iran University of Science and Technology', 'Jordan University of Science and Technology'],
    ['The University of Western Australia', 'University of Western Australia'],
    ['The University of Western Ontario', 'University of Western Ontario']
])


# def naive_pairwise():
#     print()

#     for i in range(len(UNIVERSITIES)):
#         A  = list(tokenizer(UNIVERSITIES[i]))

#         for j in range(i + 1, len(UNIVERSITIES)):
#             B = list(tokenizer(UNIVERSITIES[j]))

#             if binary_cosine_similarity(A, B) >= 0.9:
#                 print([UNIVERSITIES[i], UNIVERSITIES[j]])

# naive_pairwise()


class TestPPJoin(object):
    def test_jaccard(self):
        for kwargs in CLUSTERINGS:
            pairs = Clusters(ppjoin(UNIVERSITIES, 0.8, metric='jaccard', tokenizer=tokenizer, **kwargs))

            assert pairs == JACCARD_5_GRAMS_T8_PAIRS

            for A, B in pairs:
                assert jaccard_similarity(tokenizer(A), tokenizer(B)) >= 0.8

    def test_dice(self):
        for kwargs in CLUSTERINGS:
            pairs = Clusters(ppjoin(UNIVERSITIES, 0.85, metric='dice', tokenizer=tokenizer, **kwargs))

            assert pairs == DICE_5_GRAMS_T85_PAIRS

            for A, B in pairs:
                assert dice_coefficient(tokenizer(A), tokenizer(B)) >= 0.85

    def test_binary_cosine(self):
        for kwargs in CLUSTERINGS:
            pairs = Clusters(ppjoin(UNIVERSITIES, 0.9, metric='binary_cosine', tokenizer=tokenizer, **kwargs))

            assert pairs == BINARY_COSINE_5_GRAMS_T9_PAIRS

            for A, B in pairs:
                assert binary_cosine_similarity(tokenizer(A), tokenizer(B)) >= 0.9
