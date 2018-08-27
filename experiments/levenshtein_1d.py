import csv
from fog.key import levenshtein_1d
from Levenshtein import distance as levenshtein
from fog.clustering import key_collision, pairwise

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

# print(len(artists))

# pairwise_clusters = list(pairwise(artists, distance=levenshtein, radius=1, processes=8))
# key_clusters = list(key_collision(artists, keys=levenshtein_1d))

# print(len(pairwise_clusters) == len(key_clusters))

# A = set()
# B = set()

# for c in pairwise_clusters:
#     A.update(c)

# for c in key_clusters:
#     B.update(c)

# print(A == B)

class TrieNode(object):
    def __init__(self):
        self.children = None
        self.jumps = None
        self.leaf = None

class Trie(object):
    def __init__(self):
        self.root = TrieNode()

    def add(self, string):
        last_node = None
        node = self.root

        for c in string:
            if node.children is None:
                node.children = {c: TrieNode()}
            else:
                if c not in node.children:
                    node.children[c] = TrieNode()

            if last_node is not None:
                if last_node.jumps is None:
                    last_node.jumps = {c: node}
                else:
                    last_node.jumps[c] = node

            # NOTE: can optimize one lookup
            last_node = node
            node = node.children[c]

        node.leaf = string

    def lookup(self, string):
        stack = [(self.root, 0, False)]

        while len(stack) != 0:
            node, i, cost = stack.pop()
            c = string[i]
            print(c, node.children)
            if node.leaf:
                yield node.leaf

            if i == len(string) - 1:
                continue

            if node.children is not None and c in node.children:
                stack.append((node.children[c], i + 1, cost))


trie = Trie()
for artist in artists:
    trie.add(artist)

print(trie.root.children)

for match in trie.lookup('Vitaa'):
    print(match)

print(trie.root.children['V'].children['i'].children['t'].children['a'].children['a'].leaf)
