# =============================================================================
# Fog Graph Utils Unit Tests
# =============================================================================
import pytest

import networkx as nx
from fog.graph.utils import (
    component_sizes,
    second_largest_component_size
)


def create_components():
    g = nx.Graph()

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(1, 5)

    g.add_edge(6, 7)
    g.add_edge(6, 8)

    g.add_node(9)

    return g


class TestGraphProjection(object):
    def test_component_sizes(self):
        g = create_components()

        sizes = sorted(component_sizes(g))

        assert sizes == [1, 3, 5]

    def test_second_largest_component_size(self):
        g = nx.Graph()

        assert second_largest_component_size(g) is None

        g.add_node(1)

        assert second_largest_component_size(g) is None

        g = create_components()

        assert second_largest_component_size(g) == 3
