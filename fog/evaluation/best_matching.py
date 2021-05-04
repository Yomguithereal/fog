# =============================================================================
# Fog Best Matching Cluster Evaluation
# =============================================================================
#
# Implementation of the "best matching F1" evaluation metric.
#
# [References]:
# Yang, Y., Pierce, T., and Carbonell, J. G.  (1998). A study of retrospective
# and on-line event detection. InProc. of ACM-SIGIR, pages 28–36.
#
# Mazoyer, Béatrice, et al. "A french corpus for event detection on twitter."
# Proceedings of The 12th Language Resources and Evaluation Conference. 2020.
# https://www.aclweb.org/anthology/2020.lrec-1.763/
#
from collections import Counter
from typing import Hashable, Iterable, Tuple

from fog.utils import OnlineMean


def best_matching(
    truth: Iterable[Iterable[Hashable]],
    predicted: Iterable[Iterable[Hashable]]
) -> Tuple[float, float, float]:
    """
    Efficient implementation of the "best matching F1" evaluation metric for
    clusters.

    Args:
        truth (iterable): the truth clusters.
        predicted (iterable): the predicted clusters.

    Returns:
        tuple of floats: precision, recall and f1 score.

    """

    # We need for the truth to be indexable to speed up computations
    if not isinstance(truth, list):
        truth = list(truth)

    # Indexing truth clusters
    index = {}

    for i, cluster in enumerate(truth):
        for item in cluster:
            if item in index:
                raise TypeError('truth clusters are fuzzy (i.e. one item can be found in multiple clusters)')

            index[item] = i

    # Aggregating scores
    P = OnlineMean()
    R = OnlineMean()
    F = OnlineMean()

    for cluster in predicted:

        # Finding best matching cluster from truth
        candidates = Counter()

        for item in cluster:
            try:
                candidate_cluster_index = index[item]
            except KeyError:
                raise TypeError('predicted clusters don\'t have the same items as truth ones')

            candidates[candidate_cluster_index] += 1

        matching_cluster_index, true_positives = candidates.most_common(1)[0]
        matching_cluster = truth[matching_cluster_index]

        false_positives = len(cluster) - true_positives
        false_negatives = len(matching_cluster) - true_positives

        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1 = 2 * precision * recall / (precision + recall)  # TODO: can this mean be computed outside the loop?

        P.add(precision)
        R.add(recall)
        F.add(f1)

    return (
        float(P),
        float(R),
        float(F)
    )
