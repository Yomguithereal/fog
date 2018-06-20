# =============================================================================
# Fog Rusalka Unit Tests
# =============================================================================
from pytest import approx
from fog.key import rusalka

TESTS = [
    (('Tchekov', 'Chekhow', 'Tchekof', 'Tchekoff'), 'ʃkf'),
    (('Dzhugashvili', 'Dzhougachvili', 'Djougachvili'), 'ʒgʃfl'),
    (('Dimitrij', 'Dimitri', 'Dimitry', 'Dimitriy', 'Dmitri', 'D\'mitr', 'Dmitr'), 'dmtr')
]


class TestRusalka(object):
    def test_basics(self):

        for names, key in TESTS:
            for name in names:
                assert rusalka(name) == key
