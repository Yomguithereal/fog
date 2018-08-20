from Levenshtein import distance
from fog.metrics import levenshtein_distance, limited_levenshtein_distance
from experiments.utils import Timer

BASIC_TESTS = [
    ('book', 'back', 2),
    ('bbbbookkkk', 'bbbbackkkk', 2),
    ('hello', 'helo', 1),
    ('good sir', 'baal', 8),
    ('say', 'shiver', 5),
    ('feature', 'get-project-features', 13),
    ('example', 'samples', 3),
    ('sturgeon', 'urgently', 6),
    ('levenshtein', 'frankenstein', 6),
    ('distance', 'difference', 5),
    ('a', 'b', 1),
    ('ab', 'ac', 1),
    ('ac', 'bc', 1),
    ('abc', 'axc', 1),
    ('xabxcdxxefxgx', '1ab2cd34ef5g6', 6),
    ('a', '', 1),
    ('ab', 'a', 1),
    ('ab', 'b', 1),
    ('abc', 'ac', 1),
    ('xabxcdxxefxgx', 'abcdefg', 6),
    ('', 'a', 1),
    ('a', 'ab', 1),
    ('b', 'ab', 1),
    ('ac', 'abc', 1),
    ('abcdefg', 'xabxcdxxefxgx', 6),
    ('', '', 0),
    ('a', 'a', 0),
    ('abc', 'abc', 0),
    ('', '', 0),
    ('a', '', 1),
    ('', 'a', 1),
    ('abc', '', 3),
    ('', 'abc', 3),
    ('因為我是中國人所以我會說中文', '因為我是英國人所以我會說英文', 2)
]

RUNS = 100_000
SIZE_MULTIPLICATOR = 1

with Timer('python-Levenshtein'):
    for _ in range(RUNS):
        for A, B, _ in BASIC_TESTS:
            distance(A * SIZE_MULTIPLICATOR, B * SIZE_MULTIPLICATOR)

with Timer('fog'):
    for _ in range(RUNS):
        for A, B, _ in BASIC_TESTS:
            levenshtein_distance(A * SIZE_MULTIPLICATOR, B * SIZE_MULTIPLICATOR)

with Timer('fog-limited'):
    for _ in range(RUNS):
        for A, B, _ in BASIC_TESTS:
            limited_levenshtein_distance(1, A * SIZE_MULTIPLICATOR, B * SIZE_MULTIPLICATOR)

