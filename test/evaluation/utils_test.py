# =============================================================================
# Fog Evaluation Utils Unit Tests
# =============================================================================
from fog.evaluation import labels_to_clusters


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
