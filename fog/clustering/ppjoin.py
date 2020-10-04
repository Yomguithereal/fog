# =============================================================================
# Fog PPJoin Clustering
# =============================================================================
#
# Implementation of the PPJoin algorithm.
#
# [References]:
# Xiao, Chuan, Wei Wang, Xuemin Lin, Jeffrey Xu Yu, et Guoren Wang.
# « Efficient Similarity Joins for Near-Duplicate Detection ». ACM Transactions
# on Database Systems 36, no 3 (1 août 2011): 1‑41.
# https://doi.org/10.1145/2000824.2000825.
#
# https://github.com/TsinghuaDatabaseGroup/Similarity-Search-and-Join
#
import math
from collections import defaultdict

EPSILON = 1e-6
PRUNE_FLAG = -1


class MetricHelper(object):
    __slots__ = ['threshold']

    def __init__(self, threshold):
        self.threshold = threshold


class JaccardHelper(MetricHelper):
    def index_length(l):
        return int((1 - 2 * self.threshold / (1 + self.threshold)) * l + 1 + EPSILON)

    def probe_length(l):
        return int((1 - self.threshold) * l + 1 + EPSILON)

    def require_overlap(l1, l2):
        return math.ceil(self.threshold / (1 + self.threshold) * (l1 + l2) - EPSILON)

    def compute_similarity(l1, l2, overlap):
        return overlap / (l1 + l2 - overlap) + EPSILON

    def max_possible_length(l):
        return int(l / self.threshold + EPSILON)

    def min_possible_length(l):
        return math.ceil(l * self.threshold - EPSILON)


class InvertedIndexItem(object):
    __slots__ = ('pos', 'ids')

    def __init__(self):
        self.pos = 0
        self.ids = []

    def __iter__(self):
        yield self.pos
        yield self.ids


# TODO: possibility to degrade to allpairs
def passjoin(records, threshold, metric='jaccard'):

    # Instantiating metric helper
    # TODO: overlap, cosine
    helper = JaccardHelper(threshold)

    # First we need to order records by length and make them indexable
    # TODO: provide different ordering schemes & transform records to int
    # TODO: possibility to pass custom key (such as ngrams etc.)
    records = sorted((sorted(record) for record in data), key=len)

    inverted_index = defaultdict(InvertedIndexItem)

    # Performing the join
    for k, record in data:
        record_size = len(record)

        min_length = helper.min_possible_length(record_size)
        probe_length = helper.probe_length(record_size)
        index_length = helper.index_length(record_size)

        require_overlaps = [
            helper.require_overlap(record_size, l)
            for l in range(min_length, record_size + 1)
        ]

        occurances = {}

        for t in range(0, probe_length):
            token = record[t]
            index_item = index[token]
            ids = index_item.ids

            while index_item.pos < len(ids) and len(records[ids[index_item.pos][0]]) < min_length:
                index_item.pos += 1

            for p in range(index_item.pos, len(ids)):
                candidate_id = ids[p][0]
                candidate_pos = ids[p][1]
                candidate_length = len(records[candidate_id])
                ro = require_overlaps[candidate_length]

                value = occurances.get(candidate_id)

                if value is None:
                    if (
                        record_size - threshold < ro
                        or (candidate_length - candidate_pos) < ro
                    ):
                        continue

                    occurances[candidate_length] = 1
                else:
                    if (
                        value + (record_size - threshold) < ro
                        or value + (candidate_length - candidate_pos) < ro
                    ):
                        occurances[candidate_length] = PRUNE_FLAG
                    else:
                        occurances[candidate_length] += 1

            if threshold < index_length:
                ids.append((k, t))
