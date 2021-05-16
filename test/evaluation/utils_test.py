# =============================================================================
# Fog Evaluation Utils Unit Tests
# =============================================================================
from fog.evaluation import labels_to_clusters, clusters_to_labels


class TestEvaluationUtils(object):
    def test_labels_to_clusters(self):
        dict_labels = {
            0: 1,
            1: 1,
            2: 3,
            3: 3,
            4: 2
        }

        assert labels_to_clusters(dict_labels) == [
            [0, 1],
            [2, 3],
            [4]
        ]

        list_labels = [1, 1, 3, 3, 2]

        assert labels_to_clusters(list_labels) == [
            [0, 1],
            [2, 3],
            [4]
        ]

        assert labels_to_clusters((k * 20, v - 5) for k, v in dict_labels.items()) == [
            [0, 20],
            [40, 60],
            [80]
        ]

    def test_clusters_to_labels(self):
        clusters = [
            [0, 1],
            [2, 3],
            [4]
        ]

        assert clusters_to_labels(clusters) == {
            0: 0,
            1: 0,
            2: 1,
            3: 1,
            4: 2
        }

        assert clusters_to_labels(clusters, key=lambda x: x * 10) == {
            0: 0,
            10: 0,
            20: 1,
            30: 1,
            40: 2
        }

        clusters = [
            [2, 3],
            [0, 1],
            [4]
        ]

        assert clusters_to_labels(clusters, flat=True) == [
            1,
            1,
            0,
            0,
            2
        ]
