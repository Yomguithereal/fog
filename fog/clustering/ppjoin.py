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
    def index_length(self, l):
        return int((1 - 2 * self.threshold / (1 + self.threshold)) * l + 1 + EPSILON)

    def probe_length(self, l):
        return int((1 - self.threshold) * l + 1 + EPSILON)

    def require_overlap(self, l1, l2):
        return math.ceil(self.threshold / (1 + self.threshold) * (l1 + l2) - EPSILON)

    def compute_similarity(self, l1, l2, overlap):
        return overlap / (l1 + l2 - overlap) + EPSILON

    def max_possible_length(self, l):
        return int(l / self.threshold + EPSILON)

    def min_possible_length(self, l):
        return math.ceil(l * self.threshold - EPSILON)


class InvertedIndexItem(object):
    __slots__ = ('pos', 'ids')

    def __init__(self):
        self.pos = 0
        self.ids = []

    def __iter__(self):
        yield self.pos
        yield self.ids


def compute_overlap(x, y, require_overlap):
    lx = len(x)
    ly = len(y)

    posx = 0
    posy = 0
    current_overlap = 0

    while posx < lx and posy < ly:
        if (
            lx - posx + current_overlap < require_overlap
            or ly - posy + current_overlap < require_overlap
        ):
            return -1

        if x[posx] == y[posy]:
            current_overlap += 1
            posx += 1
            posy += 1
        elif x[posx] < y[posy]:
            posx += 1
        else:
            posy += 1

        return current_overlap


# TODO: possibility to degrade to allpairs
def ppjoin(records, threshold, metric='jaccard'):

    # Instantiating metric helper
    # TODO: overlap, cosine
    helper = JaccardHelper(threshold)

    # First we need to order records by length and make them indexable
    # TODO: provide different ordering schemes & transform records to int
    # TODO: possibility to pass custom key (such as ngrams etc.)
    records = sorted((sorted(record) for record in records), key=len)

    # State
    inverted_index = defaultdict(InvertedIndexItem)

    def pairs():

        # Performing the join
        for k, record in enumerate(records):
            record_size = len(record)

            min_length = helper.min_possible_length(record_size)
            probe_length = helper.probe_length(record_size)
            index_length = helper.index_length(record_size)

            require_overlaps = [0] * (record_size + 1)

            for l in range(min_length, record_size + 1):
                require_overlaps[l] = helper.require_overlap(record_size, l)

            occurances = {}

            for t in range(0, probe_length):
                token = record[t]
                index_item = inverted_index[token]
                ids = index_item.ids

                while index_item.pos < len(ids) and len(records[ids[index_item.pos][0]]) < min_length:
                    index_item.pos += 1

                for p in range(index_item.pos, len(ids)):
                    candidate_id = ids[p][0]
                    candidate_pos = ids[p][1]
                    candidate_length = len(records[candidate_id])

                    require_overlap = require_overlaps[candidate_length]

                    value = occurances.get(candidate_id)

                    if value is None:
                        if (
                            record_size - threshold < require_overlap
                            or (candidate_length - candidate_pos) < require_overlap
                        ):
                            continue

                        occurances[candidate_id] = 1
                    else:
                        if (
                            value + (record_size - threshold) < require_overlap
                            or value + (candidate_length - candidate_pos) < require_overlap
                        ):
                            occurances[candidate_id] = PRUNE_FLAG
                        else:
                            occurances[candidate_id] += 1

                if threshold < index_length:
                    ids.append((k, t))

            for candidate, count in occurances.items():
                if count == PRUNE_FLAG:
                    continue

                candidate_record = records[candidate]
                candidate_size = len(candidate_record)
                require_overlap = require_overlaps[candidate_size]
                index_length = helper.index_length(candidate_size)

                if candidate_record[index_length - 1] < record[probe_length - 1]:
                    if count + candidate_size - index_length < require_overlap:
                        continue
                else:
                    if count + record_size - probe_length < require_overlap:
                        continue

                real_overlap = compute_overlap(record, candidate_record, require_overlap)

                if real_overlap == -1:
                    continue

                similarity = helper.compute_similarity(record_size, candidate_size, real_overlap)

                if similarity >= threshold:
                    yield k, candidate

    return list(pairs())