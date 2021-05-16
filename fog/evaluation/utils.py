# =============================================================================
# Fog Evaluation Utils
# =============================================================================
#
# Miscellaneous helper functions related to evaluation.
#
from sys import version_info
from collections import OrderedDict
from collections.abc import Mapping, Sequence

AT_LEAST_PY37 = version_info >= (3, 7)
ordered_dict = dict if AT_LEAST_PY37 else OrderedDict


def labels_to_clusters(labels):
    clusters = ordered_dict()

    iterator = labels

    if isinstance(labels, Mapping):
        iterator = labels.items()
    elif isinstance(labels, Sequence):
        iterator = enumerate(labels)

    for i, l in iterator:
        c = clusters.get(l)

        if c is None:
            c = []
            clusters[l] = c

        c.append(i)

    return list(clusters.values())


def clusters_to_labels(clusters, *, key=None, flat=False):
    labels = {}

    for i, cluster in enumerate(clusters):
        for item in cluster:
            k = item

            if key is not None:
                k = key(item)

            labels[k] = i

    if flat:
        flat_labels = [-1] * len(labels)

        for i, l in labels.items():
            flat_labels[i] = l

        return flat_labels

    return labels
