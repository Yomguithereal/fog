# =============================================================================
# Fog Best Matching Cluster Evaluation Unit Tests
# =============================================================================
from pytest import approx, raises
from random import shuffle

from fog.evaluation import best_matching_macro_average


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
            best_matching_macro_average([['A1']], [['A2']])

        with raises(TypeError, match='fuzzy'):
            best_matching_macro_average([['A1', 'B1']], [['A1'], ['B1'], ['A1']])

        with raises(TypeError, match='empty'):
            best_matching_macro_average([['A1'], []], [['A1']])

        with raises(TypeError, match='empty'):
            best_matching_macro_average([['A1']], [['A1'], []])

        with raises(TypeError, match='truth is empty'):
            best_matching_macro_average([], [['A1']])

        with raises(TypeError, match='predicted is empty'):
            best_matching_macro_average([['A1']], [])

        with raises(TypeError, match='cannot be found'):
            best_matching_macro_average([['A1']], [['A1', 'B1']])

    def test_basics(self):
        result = best_matching_macro_average(TRUTH, CLUSTERS)

        assert result == approx((
            0.687,
            0.875,
            0.756
        ), rel=1e-2)

        assert best_matching_macro_average(TRUTH, CLUSTERS) == best_matching_macro_average(TRUTH, CLUSTERS_WITH_ADDITIONAL_ITEMS, allow_additional_items=True)

    def test_deterministic(self):
        shuffled_clusters = CLUSTERS.copy()
        shuffled_truth = TRUTH.copy()

        for _ in range(10):
            shuffle(shuffled_clusters)
            shuffle(shuffled_truth)

            assert best_matching_macro_average(shuffled_truth, shuffled_clusters) == best_matching_macro_average(TRUTH, CLUSTERS)

    def test_identity(self):
        result = best_matching_macro_average(TRUTH, TRUTH)
        assert result == approx((1.0, 1.0, 1.0))

        result = best_matching_macro_average(CLUSTERS, CLUSTERS)
        assert result == approx((1.0, 1.0, 1.0))
