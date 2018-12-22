import csv
import random
from collections import defaultdict
from functools import partial
from statistics import median, mean
from timeit import default_timer as timer
from fog.clustering import blocking
from fog.tokenizers import ngrams
from fog.key import levenshtein_1d_blocks, damerau_levenshtein_1d_blocks, levenshtein_2d_blocks
from fog.metrics import levenshtein_distance_lte1
from experiments.levenshtein_split import keys as generic_levenshtein_blocks

NB_CLUSTERS = 138
GROUND_TRUTH = 294

with open('./data/musicians.csv', 'r') as f:
    artists = set(line['artist'] for line in csv.DictReader(f))

print('Number of distinct artists: %i' % len(artists))
print()

def test_blocking_method(name, fn):
    blocks = defaultdict(list)

    print('%s:' % name)

    for artist in artists:
        for b in fn(artist):
            blocks[b].append(artist)

    start = timer()
    clusters = list(blocking(artists, blocks=fn, similarity=levenshtein_distance_lte1))
    time = timer() - start

    items = set()

    for c in clusters:
        items.update(c)

    max_block = max(blocks.items(), key=lambda x: len(x[1]))
    sample = random.sample(max_block[1], min(len(max_block[1]), 5))

    print('  - Number of blocks: %i' % len(blocks))
    print('  - Median size of blocks: %f' % median(len(b) for b in blocks.values()))
    print('  - Median size of colliding blocks: % f' % median(len(b) for b in blocks.values() if len(b) > 1))
    print('  - Mean size of blocks: %f' % mean(len(b) for b in blocks.values()))
    print('  - Max size of blocks: %i' % len(max_block[1]))
    print('  - Key of max block: "%s"' % str(max_block[0]))
    print('  - Sample of max block:')

    for element in sample:
        print('     * "%s"' % element)

    print('  - Recall %f' % (len(items) / GROUND_TRUTH))
    print('  - Time %f' % time)
    print()

test_blocking_method('Levenshtein 1D Blocks', levenshtein_1d_blocks)
test_blocking_method('Damerau-Levenshtein 1D Blocks', damerau_levenshtein_1d_blocks)
test_blocking_method('Levenshtein 2D Blocks', levenshtein_2d_blocks)
test_blocking_method('Levenshtein 3D Blocks', partial(generic_levenshtein_blocks, 3))
test_blocking_method('Levenshtein 4D Blocks', partial(generic_levenshtein_blocks, 4))
test_blocking_method('Levenshtein 5D Blocks', partial(generic_levenshtein_blocks, 5))
test_blocking_method('4-grams Blocks', partial(ngrams, 4))
test_blocking_method('5-grams Blocks', partial(ngrams, 5))
test_blocking_method('6-grams Blocks', partial(ngrams, 6))
test_blocking_method('7-grams Blocks', partial(ngrams, 7))
test_blocking_method('8-grams Blocks', partial(ngrams, 8))
