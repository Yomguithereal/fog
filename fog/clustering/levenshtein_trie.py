# =============================================================================
# Fog Levensthein Trie Clustering
# =============================================================================
#
# Clustering algorithm leveraging a Trie to perform more efficient
# Levensthein distance computations.
#
# Note that while this is a compelling solution for single searches, this
# does not scale well at all for the clustering case, since pairwise is
# basically faster.
#
# [Url]:
# http://stevehanov.ca/blog/index.php?id=114
#
from fog.clustering.utils import clusters_from_pairs


class TrieNode(object):

    __slots__ = ('children', 'index')

    def __init__(self, index=None):
        self.children = None
        self.index = index


class Trie(object):

    def __init__(self):

        self.root = TrieNode()

    def add(self, index, string):

        node = self.root

        for stem in string:

            if node.children is None:
                node.children = {}

            child = node.children.get(stem)

            if child is None:
                child = TrieNode()
                node.children[stem] = child

            node = child

        node.index = index

    def search(self, string, radius):
        if self.root.children is None:
            return

        columns = len(string) + 1
        stack = []

        for root_stem, root_child in self.root.children.items():
            stack.append((root_child, root_stem, range(len(string) + 1)))

            while len(stack) != 0:
                node, stem, previous_row = stack.pop()

                current_row = [previous_row[0] + 1]

                for column in range(1, columns):

                    insert_cost = current_row[column - 1] + 1
                    delete_cost = previous_row[column] + 1
                    replace_cost = previous_row[column - 1] + (1 if string[column - 1] != stem else 0)

                    current_row.append(min(insert_cost, delete_cost, replace_cost))

                # Match?
                if current_row[-1] <= radius and node.index is not None:
                    yield (current_row[-1], node.index)

                # Following
                if min(current_row) <= radius and node.children is not None:
                    for child_stem, child in node.children.items():
                        stack.append((child, child_stem, current_row))


def levenshtein_trie(data, radius=2, min_size=2, max_size=float('inf'),
                     mode='connected_components'):
    """
    Function returning an iterator over found clusters by leveraging a Trie
    to perform more efficient Levenshtein distance computations.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        radius (number, optional): produced clusters' radius.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.

    Yields:
        list: A viable cluster.

    """

    # Indexing data
    trie = Trie()

    if type(data) is not list:
        data = list(data)

    for i, item in enumerate(data):
        trie.add(i, item)

    def clustering():
        for i, item in enumerate(data):
            for d, j in trie.search(item, radius):
                if i == j:
                    continue

                yield (i, j)

    gen = clusters_from_pairs(
        clustering(),
        min_size=min_size,
        max_size=max_size,
        mode=mode,
        fuzzy=True
    )

    for cluster in gen:
        yield [data[i] for i in cluster]
