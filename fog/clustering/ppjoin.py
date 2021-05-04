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
# https://web.archive.org/web/20170624090246/http://www.cse.unsw.edu.au/~weiw/project/simjoin.html
#
# https://github.com/TsinghuaDatabaseGroup/Similarity-Search-and-Join
# http://www.vldb.org/pvldb/vol9/p636-mann.pdf
#
import math
from collections import defaultdict, Counter
from bisect import bisect_left
from ebbe import sorted_uniq

from fog.lsh.utils import crc32

EPSILON = 1e-6
PRUNE_FLAG = -1
MAX_DEPTH = 2

TOKEN_ORDERINGS = ('freq', 'crc32')


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


class DiceHelper(MetricHelper):
    def index_length(self, l):
        return int((1 - self.threshold) * l + 1 + EPSILON)

    def probe_length(self, l):
        return int((1 - self.threshold / (2 - self.threshold)) * l + 1 + EPSILON)

    def require_overlap(self, l1, l2):
        return math.ceil((l1 + l2) * self.threshold / 2.0 - EPSILON)

    def compute_similarity(self, l1, l2, overlap):
        return 2 * overlap / (l1 + l2) + EPSILON

    def max_possible_length(self, l):
        return int(l / self.threshold * (2 - self.threshold) + EPSILON)

    def min_possible_length(self, l):
        return math.ceil(l * self.threshold / (2 - self.threshold) - EPSILON)


class BinaryCosineHelper(MetricHelper):
    def index_length(self, l):
        return int((1 - self.threshold) * l + 1 + EPSILON)

    def probe_length(self, l):
        return int((1 - self.threshold * self.threshold) * l + 1 + EPSILON)

    def require_overlap(self, l1, l2):
        return math.ceil(self.threshold * math.sqrt(l1 * l2) - EPSILON)

    def compute_similarity(self, l1, l2, overlap):
        return overlap / math.sqrt(l1 * l2) + EPSILON

    def max_possible_length(self, l):
        return int(l / self.threshold / self.threshold + EPSILON)

    def min_possible_length(self, l):
        return math.ceil(l * self.threshold * self.threshold - EPSILON)


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


def suffix_filter(x, y, x_start, x_end, y_start, y_end, hd, depth=0):
    x_len = x_end - x_start
    y_len = y_end - y_start

    if x_end <= x_start or y_end <= y_start:
        return abs(x_len - y_len)

    left = 0
    right = 0
    offset = 0

    hd_left = 0
    hd_right = 0
    hd_left_bound = 0
    hd_right_bound = 0

    mid = x_start + x_len // 2
    token = x[mid]

    if x_len >= y_len:
        delta = x_len - y_len
        offset = (hd - delta) // 2 + delta
        left = y_start + x_len // 2 - offset
        offset = (hd - delta) // 2
        right = y_start + x_len // 2 + offset
    else:
        delta = y_len - x_len
        offset = (hd - delta) // 2
        left = y_start + x_len // 2 - offset
        offset = (hd - delta) // 2 + delta
        right = y_start + x_len // 2 + offset

    if (
        (left >= y_start and y[left] > token)
        or (right < y_end and y[right] < token)
    ):
        return hd + 1

    search_left = left if left >= y_start else y_start
    search_right = right + 1 if right + 1 < y_end else y_end

    pos = bisect_left(y, token, search_left, search_right)

    if pos < y_end and y[pos] == token:
        hd_left = hd_left_bound = abs((mid - x_start) - (pos - y_start))
        hd_right = hd_right_bound = abs((x_end - mid - 1) - (y_end - pos - 1))

        if hd_left_bound + hd_right_bound > hd:
            return hd_left_bound + hd_right_bound

        if depth < MAX_DEPTH:
            hd_left = suffix_filter(x, y, x_start, mid, y_start, pos, hd - hd_right_bound, depth + 1)

            if hd_left + hd_right_bound > hd:
                return hd_left + hd_right_bound

            hd_right = suffix_filter(x, y, mid + 1, x_end, pos + 1, y_end, hd - hd_left, depth + 1)

        return hd_left + hd_right
    else:
        hd_left = hd_left_bound = abs((mid - x_start) - (pos - y_start))
        hd_right = hd_right_bound = abs((x_end - mid - 1) - (y_end - pos))

        if hd_left_bound + hd_right_bound + 1 > hd:
            return hd_left_bound + hd_right_bound + 1

        if depth < MAX_DEPTH:
            hd_left = suffix_filter(x, y, x_start, mid, y_start, pos, hd - hd_right_bound - 1, depth + 1)

            if hd_left + hd_right_bound + 1 > hd:
                return hd_left + hd_right_bound + 1

            hd_right = suffix_filter(x, y, mid + 1, x_end, pos, y_end, hd - hd_left - 1, depth + 1)

        return hd_left + hd_right + 1

    return 0


def preprocess(records, tokenizer=None, token_ordering=None):
    freqs = Counter()
    tokenized_records = []

    for record in records:
        if tokenizer is not None:
            record = tokenizer(record)

            if not isinstance(record, list):
                record = list(record)

            if token_ordering == 'freq':
                for token in record:
                    freqs[token] += 1

        record = sorted_uniq(record)

        if token_ordering == 'crc32':
            record = sorted(crc32(token) for token in record)

        tokenized_records.append(record)

    if token_ordering == 'freq':
        labels = {token: i for i, (token, _) in enumerate(sorted(freqs.items(), key=lambda x: (x[1], x[0])))}

        tokenized_records = [
            sorted(labels[token] for token in record)
            for record in tokenized_records
        ]

    argsort = sorted(range(len(tokenized_records)), key=lambda i: len(tokenized_records[i]))

    return tokenized_records, argsort


def ppjoin(records, threshold, metric='jaccard', tokenizer=None, all_pairs=False,
           plus=False, token_ordering='freq'):
    """
    Function returning an iterator over similar pairs of records found using
    the All-Pairs, PPJoin or PPJoin+ algorithm.

    Args:
        records (iterable): The records to work on.
        threshold (float): The similarity threshold under which pairs of
            records won't be deemed similar enough.
        metric (str, optional): The similarity metric to use. Can be `jaccard`,
            `dice` or `binary_cosine`. Defaults to `jaccard`.
        tokenizer (callable, optional): An optional tokenizer function processing
            the records, such as ngrams etc. Defaults to `None`.
        all_pairs (bool, optional): Whether to avoid leveraging PPJoin's
            filtering strategies and only apply the simpler All-Pairs
            algorithm instead. Defaults to `False`.
        plus (bool, optional): Whether to use PPJoin+'s suffix filtering.
            Defaults to `False`.
        token_ordering (str, optional): Which kind of token global ordering
            to use when sorting tokens for prefix filtering. Can be `None`,
            `freq` or `crc32`. `None` mean sorting will be done alphabetically.
            `freq` will sort tokens by increasing corpus frequency to
            minimize collisions. Finally `crc32` will map tokens to their crc32
            hash, meaning the order will be random. Defaults to `freq`.

    Yields:
        tuple: A similar pair.

    """

    if tokenizer is not None and not callable(tokenizer):
        raise TypeError('fog.clustering.ppjoin: tokenizer is not callable')

    if token_ordering is not None and token_ordering not in TOKEN_ORDERINGS:
        raise TypeError('fog.clustering.ppjoin: unknown token ordering "%s"' % token_ordering)

    # Instantiating metric helper
    if metric == 'jaccard':
        helper = JaccardHelper(threshold)
    elif metric == 'dice':
        helper = DiceHelper(threshold)
    elif metric == 'binary_cosine':
        helper = BinaryCosineHelper(threshold)
    else:
        raise TypeError('fog.clustering.ppjoin: unsupported metric "%s"' % metric)

    # First we need to order records by length and make them indexable
    if not isinstance(records, list):
        records = list(records)

    tokenized_records, argsort = preprocess(records, tokenizer, token_ordering)

    # State
    inverted_index = defaultdict(InvertedIndexItem)

    # Performing the join
    for k in argsort:
        record = tokenized_records[k]
        record_length = len(record)

        min_length = helper.min_possible_length(record_length)
        probe_length = helper.probe_length(record_length)
        index_length = helper.index_length(record_length)

        # NOTE: maybe we could try avoiding storing this in memory?
        require_overlaps = [0] * (record_length + 1)

        for l in range(min_length, record_length + 1):
            require_overlaps[l] = helper.require_overlap(record_length, l)

        occurances = {}

        for t in range(0, probe_length):
            token = record[t]
            index_item = inverted_index[token]
            ids = index_item.ids

            while index_item.pos < len(ids) and len(tokenized_records[ids[index_item.pos][0]]) < min_length:
                index_item.pos += 1

            for p in range(index_item.pos, len(ids)):
                candidate_id = ids[p][0]

                if all_pairs:
                    if candidate_id not in occurances:
                        occurances[candidate_id] = 1
                    else:
                        occurances[candidate_id] += 1

                    continue

                candidate_pos = ids[p][1]
                candidate_length = len(tokenized_records[candidate_id])

                require_overlap = require_overlaps[candidate_length]

                value = occurances.get(candidate_id)

                # NOTE: this should be here in principle, but it does not change much?
                if value == PRUNE_FLAG:
                    continue

                # Suffix filtering
                if plus:
                    hamming_distance = (
                        candidate_length +
                        record_length -
                        2 * require_overlap +
                        (0 if value is None else 2 * value) -
                        (candidate_pos + t)
                    )

                    # NOTE: I am not completely sure I am not missing something here...
                    if hamming_distance >= 0:
                        sf = suffix_filter(
                            tokenized_records[candidate_id],
                            record,
                            candidate_pos,
                            candidate_length,
                            t,
                            record_length,
                            hamming_distance
                        )

                        if sf > hamming_distance:
                            if value is not None:
                                occurances[candidate_id] = PRUNE_FLAG

                            continue

                if value is None:
                    if (
                        record_length - threshold < require_overlap
                        or (candidate_length - candidate_pos) < require_overlap
                    ):
                        continue

                    occurances[candidate_id] = 1
                else:
                    if (
                        value + (record_length - threshold) < require_overlap
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

            candidate_record = tokenized_records[candidate]
            candidate_size = len(candidate_record)
            require_overlap = require_overlaps[candidate_size]
            index_length = helper.index_length(candidate_size)

            if candidate_record[index_length - 1] < record[probe_length - 1]:
                if count + candidate_size - index_length < require_overlap:
                    continue
            else:
                if count + record_length - probe_length < require_overlap:
                    continue

            real_overlap = compute_overlap(record, candidate_record, require_overlap)

            if real_overlap == -1:
                continue

            similarity = helper.compute_similarity(record_length, candidate_size, real_overlap)

            if similarity >= threshold:
                yield records[k], records[candidate]


def all_pairs(records, threshold, metric='jaccard', tokenizer=None,
              token_ordering='freq'):
    return ppjoin(
        records,
        threshold,
        metric=metric,
        tokenizer=tokenizer,
        token_ordering=token_ordering,
        all_pairs=True
    )


def ppjoin_plus(records, threshold, metric='jaccard', tokenizer=None,
                token_ordering='freq'):
    return ppjoin(
        records,
        threshold,
        metric=metric,
        tokenizer=tokenizer,
        token_ordering=token_ordering,
        plus=True
    )
