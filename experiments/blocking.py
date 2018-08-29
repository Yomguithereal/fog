import csv
from collections import defaultdict
from functools import partial
from statistics import median, mean
from fog.tokenizers import ngrams
from fog.key import levenshtein_1d_blocks

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

print('Number of distinct artists: %i' % len(artists))
print()

def test_blocking_method(name, fn):
    blocks = defaultdict(list)

    for artist in artists:
        for b in fn(artist):
            blocks[b].append(artist)

    print('%s:' % name)
    print('  - Number of blocks: %i' % len(blocks))
    print('  - Median size of blocks: %f' % median(len(b) for b in blocks.values()))
    print('  - Mean size of blocks: %f' % mean(len(b) for b in blocks.values()))
    print('  - Max size of blocks: %i' % max(len(b) for b in blocks.values()))
    print()

test_blocking_method('Levenshtein 1D Blocks', levenshtein_1d_blocks)
test_blocking_method('5-grams Blocks', partial(ngrams, 5))
test_blocking_method('6-grams Blocks', partial(ngrams, 6))
test_blocking_method('7-grams Blocks', partial(ngrams, 7))
test_blocking_method('8-grams Blocks', partial(ngrams, 8))
