# =============================================================================
# Fog Omission Key Unit Tests
# =============================================================================
from fog.key import omission_key

TESTS = [
    ('', ''),
    ('hello', 'HLEO'),
    ('The quick brown fox jumped over the lazy dog.', 'JKQXZVWYBFMGPDHCLNTREUIOA'),
    ('Christopher', 'PHCTSRIOE'),
    ('Niall', 'LNIA'),
    ('caramel', 'MCLRAE'),
    ('Carlson', 'CLNSRAO'),
    ('Karlsson', 'KLNSRAO'),
    ('microeletronics', 'MCLNTSRIOE'),
    ('Circumstantial', 'MCLNTSRIUA'),
    ('LUMINESCENT', 'MCLNTSUIE'),
    ('multinucleate', 'MCLNTUIEA'),
    ('multinucleon', 'MCLNTUIEO'),
    ('cumulene', 'MCLNUE'),
    ('luminance', 'MCLNUIAE'),
    ('cœlomic', 'MCLOEI'),
    ('Molecule', 'MCLOEU'),
    ('Cameral', 'MCLRAE'),
    ('Maceral', 'MCLRAE'),
    ('Lacrimal', 'MCLRAI')
]


class TestOmissionKey(object):
    def test_basics(self):

        for string, key in TESTS:
            assert omission_key(string) == key, '%s => %s' % (string, key)
