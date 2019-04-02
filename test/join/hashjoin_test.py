from fog.join import hashjoin


B = [
    'John Doe',
    'Ron Wisley',
    'Clark Kent',
    'Britney Spears',
]

A = [
    'Spartan Spears',
    'Kent & Barby',
    'Doe John',
    'Ron The Turtel',
    'Kent Doe',
    'John Mirage',
    'Mirage',
]

R = [
    ('John Doe', 'Doe John'),
    ('John Doe', 'Kent Doe'),
    ('John Doe', 'John Mirage'),
    ('Ron Wisley', 'Ron The Turtel'),
    ('Clark Kent', 'Kent & Barby'),
    ('Clark Kent', 'Kent Doe'),
    ('Britney Spears', 'Spartan Spears')
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


def fingerprint(item):
    item = item.lower()
    item = item.split(' ')
    return [k.strip() for k in item]


def fingerprintObj(item):
    item = item['name'].lower()
    item = item.split(' ')
    return [k.strip() for k in item]


class TestHashJoin(object):

    def simpleTest(self):
        result = list(hashjoin(A, B, keys=fingerprint))
        assert result == R

    def objectTest(self):
        result = list(hashjoin(objA, objB, keys=fingerprintObj))
        assert result == objR
