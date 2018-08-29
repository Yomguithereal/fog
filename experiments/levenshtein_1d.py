import csv
from experiments.utils import Timer
from fog.key import levenshtein_1d_keys, levenshtein_1d_blocks
from Levenshtein import distance as levenshtein
from fog.clustering import key_collision, pairwise, blocking
from fog.metrics import levenshtein_distance_lte1

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

print(len(artists))

with Timer('pairwise'):
    pairwise_clusters = list(pairwise(artists, distance=levenshtein, radius=1, processes=8))

with Timer('keys'):
    key_clusters = list(key_collision(artists, keys=levenshtein_1d_keys))

with Timer('blocks'):
    block_clusters = list(blocking(artists, blocks=levenshtein_1d_blocks, similarity=levenshtein_distance_lte1))

print(len(pairwise_clusters) == len(key_clusters) == len(block_clusters))

A = set()
B = set()
C = set()

for c in pairwise_clusters:
    A.update(c)

for c in key_clusters:
    B.update(c)

for c in block_clusters:
    C.update(c)

print(A == B == C)


# # TODO: try a radix tree instead?

# class TrieNode(object):
#     def __init__(self):
#         self.children = None
#         self.jumps = None
#         self.leaf = None

# class Trie(object):
#     def __init__(self):
#         self.root = TrieNode()

#     def add(self, string):
#         last_node = None
#         node = self.root
#         last_node = None

#         for c in string:
#             if node.children is None:
#                 node.children = {c: TrieNode()}
#             else:
#                 if c not in node.children:
#                     node.children[c] = TrieNode()

#             if last_node is not None:
#                 if last_node.jumps is None:
#                     last_node.jumps = {c: node.children[c]}
#                 else:
#                     last_node.jumps[c] = node.children[c]

#             # NOTE: can optimize one lookup
#             last_node = node
#             node = node.children[c]

#         node.leaf = string

#     def lookup(self, string):
#         stack = [(self.root, -1, None)]

#         o = 0
#         while len(stack) != 0:
#             o += 1
#             node, i, op = stack.pop()

#             # NOTE: op None is skippable if not searching self
#             if op is None and i == len(string) - 1:
#                 continue

#                 if node.leaf:
#                     yield node.leaf

#                 continue

#             if op == 'sub' and i == len(string) - 1:

#                 if node.leaf:
#                     yield node.leaf

#                 continue

#             if op == 'add' and i == len(string) - 1:

#                 if node.leaf:
#                     yield node.leaf

#                 continue

#             c = string[i + 1]

#             if node.children is not None and c in node.children:
#                 stack.append((node.children[c], i + 1, op))

#             # Can we fork?
#             if op is None and node.children is not None:
#                 for l, child in node.children.items():
#                     if l == c:
#                         continue

#                     # if i + 2 < len(string) - 1 and child.jumps is not None and string[i + 2] not in child.jumps:
#                     #     continue

#                     # TODO: compress this into a single call
#                     stack.append((child, i + 1, 'sub'))
#                     # stack.append((child, i, 'add'))

#                 if node.jumps is not None and c in node.jumps:
#                     stack.append((node.jumps[c], i + 1, 'add'))

#             # Using jumps

#         # print(o)

# with Timer('Trie'):
#     trie = Trie()
#     for artist in artists:
#         trie.add(artist)

#     # print(trie.root.children)

#     # for match in trie.lookup('Vitaa'):
#     #     print(match)

#     # print()
#     # for match in trie.lookup('Vasko Vasilev'):
#     #     print(match)

#     # TODO: insert artists in triangular order, only after lookup for backwards relation & streaming
#     # TODO: ^ requires to sort by length
#     for artist in artists:
#         for match in trie.lookup(artist):
#             # print((artist, match))
#             pass
