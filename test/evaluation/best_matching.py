# =============================================================================
# Fog Best Matching Cluster Evaluation Unit Tests
# =============================================================================
from pytest import approx, raises

from fog.evaluation import best_matching


TRUTH = [
    ['A1', 'A2', 'A3'],
    ['B1', 'B2'],
    ['C1'],
    ['D1', 'D2', 'D3', 'D4']
]

CLUSTERS = [
    ['A1', 'B1', 'A2', 'A3'],
    ['B2', 'C1'],
    ['D1', 'D2', 'D3', 'D4']
]


class TestBestMatching(object):
    def test_exceptions(self):
        with raises(TypeError, match='same item'):
            best_matching([['A1']], [['A2']])

        with raises(TypeError, match='fuzzy'):
            best_matching([['A1'], ['B1'], ['A1']], [])

    def test_basics(self):
        result = best_matching(TRUTH, CLUSTERS)

        assert result == approx((
            0.75,
            0.83,
            0.78
        ), rel=1e-2)

    def test_identity(self):
        result = best_matching(TRUTH, TRUTH)

        assert result == approx((1.0, 1.0, 1.0))

        result = best_matching(CLUSTERS, CLUSTERS)

        assert result == approx((1.0, 1.0, 1.0))
