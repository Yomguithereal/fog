import csv
from fog.key import levenshtein_1d
from Levenshtein import distance as levenshtein
from fog.clustering import key_collision, pairwise

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

print(len(artists))

pairwise_clusters = list(pairwise(artists, distance=levenshtein, radius=1, processes=8))
key_clusters = list(key_collision(artists, keys=levenshtein_1d))

print(len(pairwise_clusters) == len(key_clusters))

A = set()
B = set()

for c in pairwise_clusters:
    A.update(c)

for c in key_clusters:
    B.update(c)

print(A == B)

# class TrieNode(object):
#     def __init__(self):
#         self.children = None
#         self.leaf = None

# class Trie(object):
#     def __init__(self):
#         self.root = TrieNode()

#     def add(self, string):
#         last_node = None
#         node = self.root

#         for c in string:
#             if node.children is None:
#                 node.children = {c: TrieNode()}
#             else:
#                 if c not in node.children:
#                     node.children[c] = TrieNode()

#             # NOTE: can optimize one lookup
#             node = node.children[c]

#         node.leaf = string

#     def lookup(self, string):
#         stack = [(self.root, -1, None)]

#         while len(stack) != 0:
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

#                     # TODO: compress this into a single call
#                     stack.append((child, i + 1, 'sub'))
#                     stack.append((child, i, 'add'))

# trie = Trie()
# for artist in artists:
#     trie.add(artist)

# # print(trie.root.children)

# # for match in trie.lookup('Vitaa'):
# #     print(match)

# # print()
# # for match in trie.lookup('Vasko Vasilev'):
# #     print(match)

# # TODO: insert artists in triangular order, only after lookup for backwards relation & streaming
# # TODO: ^ requires to sort by length
# for artist in artists:
#     for match in trie.lookup(artist):
#         print((artist, match))
