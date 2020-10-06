import csv
from fog.clustering import (
    all_pairs,
    ppjoin,
    ppjoin_plus,
    pairwise_connected_components
)
from fog.tokenizers import trigrams
from fog.metrics import jaccard_similarity
from experiments.utils import Timer

JACCARD_TRIGRAMS_08_GROUND_TRUTH = [
    ('Adam Jones (musician)', 'Sam Jones (musician)'),
    ('Alan Wilson (musician)', 'Dan Wilson (musician)'),
    ('Alan Wilson (musician)', 'Ian Wilson (musician)'),
    ('Arsenie Todiraş', 'Arsenie Todiraș'),
    ('Bana (singer)', 'Jana (singer)'),
    ('Bana (singer)', 'Nana (singer)'),
    ('Barry Sparks', 'Larry Sparks'),
    ('Ben Wilson (musician)', 'Dan Wilson (musician)'),
    ('Ben Wilson (musician)', 'Ian Wilson (musician)'),
    ('Christoforos Schuff', 'Fr. Christoforos Schuff'),
    ('Dan Wilson (musician)', 'Ian Wilson (musician)'),
    ('Dana (South Korean singer)', 'Dia (South Korean singer)'),
    ('Dave Williams (musician)', 'Steve Williams (musician)'),
    ('Dick Taylor', 'Mick Taylor'),
    ('Dina (singer)', 'Mina (singer)'),
    ('Donald Braswell', 'Donald Braswell II'),
    ('Donnie Brooks', 'Lonnie Brooks'),
    ('Donnie Van Zant', 'Ronnie Van Zant'),
    ('Doyle Bramhall', 'Doyle Bramhall II'),
    ('Elissa (singer)', 'Julissa (singer)'),
    ('Eric Taylor (Brazilian musician)', 'Eric Taylor (brazilian musician)'),
    ('Evan Parker', 'Ivan Parker'),
    ('Flip Phillips', 'Phillip Phillips'),
    ('Jana (singer)', 'Nana (singer)'),
    ('Jem (singer)', 'Kem (singer)'),
    ('Jim Adams (musician)', 'Sam Adams (musician)'),
    ('Jim Ward (musician)', 'Tim Ward (musician)'),
    ('Joe (singer)', 'Poe (singer)'),
    ('John Paris', 'John Parish'),
    ('Johnny Marr', 'Johnny Mars'),
    ('K (singer)', 'KK (singer)'),
    ('La Mala Rodríguez', 'Mala Rodríguez'),
    ('Lobo (musician)', 'Robo (musician)'),
    ('Luna (singer)', 'Yuna (singer)'),
    ('Mando (singer)', 'Wando (singer)'),
    ('Paul Simon', 'Paul Simonon'),
    ('Richard Bona', 'Richard Bone'),
    ('Steve Nardella', 'Steve Nardelli'),
    ('Tim Smith (musician)', 'Tom Smith (musician)')
]

def compare(A, B):
    assert len(A) == len(B), 'len A = %i, while len B = %i' % (len(A), len(B))

    A = set(tuple(sorted(t)) for t in A)
    B = set(tuple(sorted(t)) for t in B)

    assert A == B

with open('./data/musicians.csv', 'r') as f:
    ARTISTS = set(line['artist'] for line in csv.DictReader(f) if len(line['artist'].strip()) > 0)

# ~150s
# with Timer('pairwise'):
#     clusters = list(pairwise_connected_components(ARTISTS, similarity=jaccard_similarity, radius=0.8, key=lambda x: list(trigrams(x)), processes=8))

with Timer('All-Pairs'):
    pairs = list(all_pairs(ARTISTS, 0.8, tokenizer=trigrams))

compare(pairs, JACCARD_TRIGRAMS_08_GROUND_TRUTH)

with Timer('PPJoin'):
    pairs = list(ppjoin(ARTISTS, 0.8, tokenizer=trigrams))

compare(pairs, JACCARD_TRIGRAMS_08_GROUND_TRUTH)

with Timer('PPJoin+'):
    pairs = list(ppjoin_plus(ARTISTS, 0.8, tokenizer=trigrams))

compare(pairs, JACCARD_TRIGRAMS_08_GROUND_TRUTH)
