# Little experiments testing the recall of the skeleton and omission keys
#
# Note that counting the number of clusters may be erroneous but with
# a low Levenshtein distance, clusters are rarely very large and this is
# good enough.
#
import csv
from Levenshtein import distance as levenshtein
from fog.clustering import pairwise_connected_components, sorted_neighborhood
from fog.key import skeleton_key, omission_key

GROUND_TRUTH_LEV1 = 138
GROUND_TRUTH_LEV2 = 627

with open('./data/musicians.csv', 'r') as f:
    reader = csv.DictReader(f)

    artists = sorted(set(line['artist'] for line in reader))

    print('Artists: %i' % len(artists))

    # true_clusters = list(pairwise_connected_components(artists, distance=levenshtein, radius=2, processes=8))

    # print(len(true_clusters))

    print('GroundTruth-Lev1: %i' % GROUND_TRUTH_LEV1)
    print('GroundTruth-Lev2: %i' % GROUND_TRUTH_LEV2)

    skeleton_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=1, key=skeleton_key))

    print('Skeleton-Lev1: Found %i clusters (Recall: %f)' % (len(skeleton_clusters), len(skeleton_clusters) / GROUND_TRUTH_LEV1))

    skeleton_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=2, key=skeleton_key))

    print('Skeleton-Lev2: Found %i clusters (Recall: %f)' % (len(skeleton_clusters), len(skeleton_clusters) / GROUND_TRUTH_LEV2))

    omission_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=1, key=omission_key))

    print('Omission-Lev1: Found %i clusters (Recall: %f)' % (len(omission_clusters), len(omission_clusters) / GROUND_TRUTH_LEV1))

    omission_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=2, key=omission_key))

    print('Omission-Lev2: Found %i clusters (Recall: %f)' % (len(omission_clusters), len(omission_clusters) / GROUND_TRUTH_LEV2))

    compound_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=1, keys=(omission_key, skeleton_key)))

    print('Compound-Lev1: Found %i clusters (Recall: %f)' % (len(compound_clusters), len(compound_clusters) / GROUND_TRUTH_LEV1))

    compound_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=2, keys=(omission_key, skeleton_key)))

    print('Compound-Lev2: Found %i clusters (Recall: %f)' % (len(compound_clusters), len(compound_clusters) / GROUND_TRUTH_LEV2))

    lexicographic_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=1, key=None))

    print('Lexicographic-Lev1: Found %i clusters (Recall: %f)' % (len(lexicographic_clusters), len(lexicographic_clusters) / GROUND_TRUTH_LEV1))

    lexicographic_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=2, key=None))

    print('Lexicographic-Lev2: Found %i clusters (Recall: %f)' % (len(lexicographic_clusters), len(lexicographic_clusters) / GROUND_TRUTH_LEV2))

    reverse_lexicographic_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=1, key=lambda x: x[::-1]))

    print('ReverseLexicographic-Lev1: Found %i clusters (Recall: %f)' % (len(reverse_lexicographic_clusters), len(reverse_lexicographic_clusters) / GROUND_TRUTH_LEV1))

    reverse_lexicographic_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=2, key=lambda x: x[::-1]))

    print('ReverseLexicographic-Lev2: Found %i clusters (Recall: %f)' % (len(reverse_lexicographic_clusters), len(reverse_lexicographic_clusters) / GROUND_TRUTH_LEV2))

    compound_lexicographic_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=1, keys=(None, lambda x: x[::-1])))

    print('CompoundLexicographic-Lev1: Found %i clusters (Recall: %f)' % (len(compound_lexicographic_clusters), len(compound_lexicographic_clusters) / GROUND_TRUTH_LEV1))

    compound_lexicographic_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=2, keys=(None, lambda x: x[::-1])))

    print('CompoundLexicographic-Lev2: Found %i clusters (Recall: %f)' % (len(compound_lexicographic_clusters), len(compound_lexicographic_clusters) / GROUND_TRUTH_LEV2))

    mega_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=1, keys=(None, lambda x: x[::-1])))

    print('Mega-Lev1: Found %i clusters (Recall: %f)' % (len(mega_clusters), len(mega_clusters) / GROUND_TRUTH_LEV1))

    mega_clusters = list(sorted_neighborhood(artists, distance=levenshtein, radius=2, keys=(None, lambda x: x[::-1], omission_key, skeleton_key)))

    print('Mega-Lev2: Found %i clusters (Recall: %f)' % (len(mega_clusters), len(mega_clusters) / GROUND_TRUTH_LEV2))
