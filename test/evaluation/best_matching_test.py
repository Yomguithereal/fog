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

CLUSTERS_WITH_ADDITIONAL_ITEMS = [
    ['A1', 'B1', 'A2', 'A3'],
    ['B2', 'C1', 'E1'],
    ['D1', 'D2', 'D3', 'D4', 'E2'],
    ['E3', 'E4']
]


class TestBestMatching(object):
    def test_exceptions(self):
        with raises(TypeError, match='cannot be found'):
            best_matching([['A1']], [['A2']])

        with raises(TypeError, match='fuzzy'):
            best_matching([['A1', 'B1']], [['A1'], ['B1'], ['A1']])

        with raises(TypeError, match='empty'):
            best_matching([['A1'], []], [['A1']])

        with raises(TypeError, match='empty'):
            best_matching([['A1']], [['A1'], []])

        with raises(TypeError, match='truth is empty'):
            best_matching([], [['A1']])

        with raises(TypeError, match='predicted is empty'):
            best_matching([['A1']], [])

        with raises(TypeError, match='cannot be found'):
            best_matching([['A1']], [['A1', 'B1']])

    def test_basics(self):
        result = best_matching(TRUTH, CLUSTERS)

        assert result == approx((
            0.625,
            0.875,
            0.714
        ), rel=1e-2)

        assert best_matching(TRUTH, CLUSTERS) == best_matching(TRUTH, CLUSTERS_WITH_ADDITIONAL_ITEMS, allow_additional_items=True)

    def test_micro(self):
        result = best_matching(TRUTH, CLUSTERS, micro=True)

        assert result == approx((
            0.642,
            0.9,
            0.75
        ), rel=1e-2)

        assert best_matching(TRUTH, CLUSTERS, micro=True) == best_matching(TRUTH, CLUSTERS_WITH_ADDITIONAL_ITEMS, micro=True, allow_additional_items=True)

    def test_identity(self):
        result = best_matching(TRUTH, TRUTH)
        assert result == approx((1.0, 1.0, 1.0))

        result = best_matching(CLUSTERS, CLUSTERS)
        assert result == approx((1.0, 1.0, 1.0))

        result = best_matching(TRUTH, TRUTH, micro=True)
        assert result == approx((1.0, 1.0, 1.0))

        result = best_matching(CLUSTERS, CLUSTERS, micro=True)
        assert result == approx((1.0, 1.0, 1.0))
