# =============================================================================
# Fog Graph Projection Unit Tests
# =============================================================================
import networkx as nx
from fog.graph import monopartite_projection

NODES = [
    ('John', 'people'),
    ('Mary', 'people'),
    ('Lucy', 'people'),
    ('Gabriel', 'people'),
    ('Meredith', 'people'),
    ('red', 'color'),
    ('blue', 'color'),
    ('yellow', 'color'),
    ('purple', 'color'),
    ('orange', 'color')
]

PEOPLE_PART = set([n[0] for n in NODES if n[1] == 'people'])

EDGES = [
    ('John', 'red', 1.0),
    ('John', 'purple', 3.0),
    ('Gabriel', 'yellow', 2.0),
    ('Gabriel', 'orange', 4.0),
    ('Mary', 'red', 2.0),
    ('Mary', 'yellow', 1.0),
    ('Lucy', 'red', 7.0),
    ('Lucy', 'purple', 1.0),
]

BIPARTITE = nx.Graph()

for key, part in NODES:
    BIPARTITE.add_node(key, part=part)

BIPARTITE.add_weighted_edges_from(EDGES)


class TestGraphProjection(object):
    def test_basics(self):
        mono = monopartite_projection(BIPARTITE, 'people', part='part')

        assert set(mono.nodes) == PEOPLE_PART

        assert set(mono.edges(data='weight')) == set([
            ('John', 'Mary', 1),
            ('John', 'Lucy', 2),
            ('Mary', 'Lucy', 1),
            ('Mary', 'Gabriel', 1)
        ])
