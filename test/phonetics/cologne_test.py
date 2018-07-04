# =============================================================================
# Fog Cologne Unit Tests
# =============================================================================
from pytest import approx
from fog.phonetics import cologne

TESTS = [
    ('65752682', 'Müller-Lüdenscheidt'),
    ('17863', 'Breschnew'),
    ('3412', 'Wikipedia'),
    ('4837', 'Xavier'),
    ('478237', 'Christopher'),
    ('3556', 'Wilhelm'),
    ('351', 'Philip'),
    ('1274', 'Patrick'),
    ('051742', 'Albrecht'),
    ('68', 'Mac'),
    ('64', 'Mack')
]


class TestCologne(object):
    def test_basics(self):

        for code, name in TESTS:
            assert cologne(name) == code, '%s => %s' % (name, code)

        assert cologne('Meyer') != cologne('Müller')
        assert cologne('Meyer') == cologne('Mayr')
