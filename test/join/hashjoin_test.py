from fog.join.hashjoin import hashjoin
from pprint import pprint


A = {
    'Spartan Spears',
    'Kent & Barby',
    'Doe John',
    'Ron The Turtel',
    'Kent Doe',
    'John Mirage',
    'Mirage',
}

B = {
    'John Doe',
    'Ron Wisley',
    'Clark Kent',
    'Britney Spears',
}

R = [
    ('Ron The Turtel', 'Ron Wisley'),
    ('John Mirage', 'John Doe')
]

objA = [
    {'name': 'John Doe', 'id': 0},
    {'name': 'Ron Wisley', 'id': 1},
    {'name': 'Clark Kent', 'id': 2},
    {'name': 'Britney Spears', 'id': 3}
]


objB = [
    {'name': 'Spartan Spears', 'id': 90},
    {'name': 'Kent & Barby', 'id': 91},
    {'name': 'Doe John', 'id': 92},
    {'name': 'Ron The Turtel', 'id': 93},
    {'name': 'Kent Doe', 'id': 94},
    {'name': 'John Mirage', 'id': 95},
    {'name': 'Mirage', 'id': 96}
]

objR = [
    ({'name': 'John Doe', 'id': 0}, {'name': 'Doe John', 'id': 92}),
    ({'name': 'John Doe', 'id': 0}, {'name': 'Kent Doe', 'id': 94}),
    ({'name': 'John Doe', 'id': 0}, {'name': 'John Mirage', 'id': 95}),
    ({'name': 'Ron Wisley', 'id': 1}, {'name': 'Ron The Turtel', 'id': 93}),
    ({'name': 'Clark Kent', 'id': 2}, {'name': 'Kent & Barby', 'id': 91}),
    ({'name': 'Clark Kent', 'id': 2}, {'name': 'Kent Doe', 'id': 94}),
    ({'name': 'Britney Spears', 'id': 3}, {'name': 'Spartan Spears', 'id': 90})
]

objA = (e for e in objA)


def fingerprint(item):
    item = item.lower()
    item = item.split(' ')
    return [k.strip() for k in item][0]


def fingerprintObj(item):
    item = item['name'].lower()
    item = item.split(' ')
    return [k.strip() for k in item]


class TestHashJoin(object):

    def test_simple(self):
        result = hashjoin(A, B, key=fingerprint)
        assert set(result) == set(R)

    def test_objectTest(self):
        result = list(hashjoin(objA, objB, keys=fingerprintObj))
        assert result == objR
