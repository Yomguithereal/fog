# =============================================================================
# Fog Rusalka Unit Tests
# =============================================================================
from pytest import approx
from fog.key import rusalka

TESTS = [
    (('Tchekov', 'Chekhow', 'Tchekof', 'Tchekoff'), 'ʃkf'),
    (('Dzhugashvili', 'Dzhougachvili', 'Djougachvili'), 'ʒkʃfl'),
    (('Dimitrij', 'Dimitri', 'Dimitry', 'Dimitriy', 'Dmitri', 'D\'mitr', 'Dmitr'), 'dmtr'),
    (('Alexei', 'Alexey'), 'alx'),
    (('Sergei', 'Sergey'), 'srk'),
    (('Ekaterina', 'Yekaterina'), 'jktrn'),
    (('Moussorgsky', 'Musorkgski', 'mousorgskiy', 'Moußorgsky'), 'msrksk'),
    (('Manovich', 'Manovitz', 'Manovitch'), 'mnfʃ'),
    (('Yeltsin', 'Eltsine'), 'jltsn'),
    (('Konstantine', 'Constantine'), 'knstntn'),
    (('Poutine', 'Putin'), 'ptn'),
    (('Diaghilev', 'Diaghileff', 'Diagilef'), 'dklf'),
    (('Plushchenko', 'Plushchenko'), 'plʃnk'),
    (('Rusalka', 'Roussalka'), 'rslk'),
    (('Piotr', 'Pyotr', 'Pyter'), 'ptr'),
    (('Gagarin', 'Gagarine'), 'kkrn'),
    (('Illich', 'Ilitch'), 'alʃ'),
    (('Vladimir', 'Wladimir'), 'fldmr'),
    (('Mikhail', ), 'mkl'),
    (('Onéguine', 'Oniéguine', 'Onegin'), 'ankn'),
    (('Bakhtin', ), 'bktn'),
    (('Youri', 'Yuri', 'Iouri'), 'jr'),
    (('Aleksandr', 'Alexander'), 'alxndr')
]


class TestRusalka(object):
    def test_basics(self):

        for names, key in TESTS:
            for name in names:
                assert rusalka(name) == key
