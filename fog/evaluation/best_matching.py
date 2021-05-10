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
    predicted: Iterable[Iterable[Hashable]],
    allow_additional_items: bool = False,
    macro: bool = True
) -> Tuple[float, float, float]:
    """
    Efficient implementation of the "best matching F1" evaluation metric for
    clusters.

    Args:
        truth (iterable): the truth clusters.
        predicted (iterable): the predicted clusters.
        allow_additional_items (bool, optional): Whether to allow additional items
            that don't exist in truth clusters to be found in predicted ones. Those
            additional items will then be ignored when computing the metrics instead
            of raising an error when found. Defaults to False.
        macro (bool, optional): Whether to compute the macro or the micro average
            of the evaluation metric. Defaults to True.

    Returns:
        tuple of floats: precision, recall and f1 score.

    """

    # Indexing truth clusters
    index = {}
    truth_cluster_sizes = {}

    # NOTE: I use a counter because the function accepts arbitrary (potentially lazy)
    # iterables, not just sized ones.
    c = 0

    for i, cluster in enumerate(truth):
        c += 1

        if not cluster:
            raise TypeError('truth contains an empty cluster')

        for item in cluster:
            if item in index:
                raise TypeError('truth clusters are fuzzy (i.e. one item can be found in multiple clusters)')

            index[item] = i

        truth_cluster_sizes[i] = len(cluster)

    if c == 0:
        raise TypeError('truth is empty')

    # Aggregating scores
    P = OnlineMean()
    R = OnlineMean()
    F = OnlineMean()

    micro_true_positives = 0
    micro_false_positives = 0
    micro_false_negatives = 0

    c = 0

    for cluster in predicted:
        c += 1

        if not cluster:
            raise TypeError('predicted contains an empty cluster')

        # Finding best matching cluster from truth
        candidates = Counter()
        cluster_size = 0

        for item in cluster:
            candidate_cluster_index = index.get(item)

            if candidate_cluster_index is None:
                if not allow_additional_items:
                    raise TypeError('predicted clusters don\'t have the same items as truth ones')
                else:
                    continue

            candidates[candidate_cluster_index] += 1
            cluster_size += 1

        if len(candidates) == 0:
            assert allow_additional_items
            continue

        matching_cluster_index, true_positives = candidates.most_common(1)[0]
        matching_cluster_size = truth_cluster_sizes[matching_cluster_index]

        false_positives = cluster_size - true_positives
        false_negatives = matching_cluster_size - true_positives

        if macro:
            precision = true_positives / (true_positives + false_positives)
            recall = true_positives / (true_positives + false_negatives)
            f1 = 2 * precision * recall / (precision + recall)

            P.add(precision)
            R.add(recall)
            F.add(f1)

        else:
            micro_true_positives += true_positives
            micro_false_positives += false_positives
            micro_false_negatives += false_negatives

    if c == 0:
        raise TypeError('predicted is empty')

    if macro:
        return (
            float(P),
            float(R),
            float(F)
        )

    micro_precision = micro_true_positives / (micro_true_positives + micro_false_positives)
    micro_recall = micro_true_positives / (micro_true_positives + micro_false_negatives)

    return (
        micro_precision,
        micro_recall,
        2 * micro_precision * micro_recall / (micro_precision + micro_recall)
    )
