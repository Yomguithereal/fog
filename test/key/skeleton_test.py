# =============================================================================
# Fog Skeleton Key Unit Tests
# =============================================================================
from fog.key import skeleton_key

TESTS = [
    ('', ''),
    ('hello', 'HLEO'),
    ('The quick brown fox jumped over the lazy dog.', 'THQCKBRWNFXJMPDVLZYGEUIOA'),
    ('Christopher', 'CHRSTPIOE'),
    ('Niall', 'NLIA'),
    ('CHEMOGENIC', 'CHMGNEOI'),
    ('chemomagnetic', 'CHMGNTEOAI'),
    ('Chemcal', 'CHMLEA'),
    ('Chemcial', 'CHMLEIA'),
    ('Chemical', 'CHMLEIA'),
    ('Chemicial', 'CHMLEIA'),
    ('Chimical', 'CHMLIA'),
    ('Chemiluminescence', 'CHMLNSEIU'),
    ('Chemiluminescent', 'CHMLNSTEIU'),
    ('Chemically', 'CHMLYEIA')
]


class TestSkeletonKey(object):
    def test_basics(self):

        for string, key in TESTS:
            assert skeleton_key(string) == key, '%s => %s' % (string, key)
