# =============================================================================
# Fog Graph Projection Unit Tests
# =============================================================================
import pytest
from pytest import approx

import networkx as nx
from fog.graph import monopartite_projection
from fog.metrics import (
    sparse_cosine_similarity,
    jaccard_similarity,
    overlap_coefficient
)

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


def to_vector(g, u):
    return {n: w for _, n, w in g.edges(u, data='weight')}


class TestGraphProjection(object):
    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            monopartite_projection(BIPARTITE, 'people', part='part', metric='unknown')

    def test_basics(self):
        mono = monopartite_projection(BIPARTITE, 'people', part='part')

        assert set(mono.nodes) == PEOPLE_PART

        assert set(mono.edges(data='weight')) == set([
            ('John', 'Mary', 1),
            ('John', 'Lucy', 2),
            ('Mary', 'Lucy', 1),
            ('Mary', 'Gabriel', 1)
        ])

    def test_cosine(self):
        mono = monopartite_projection(BIPARTITE, 'people', part='part', metric='cosine')

        assert set(mono.nodes) == PEOPLE_PART

        for u, v, c in mono.edges(data='weight'):
            u = to_vector(BIPARTITE, u)
            v = to_vector(BIPARTITE, v)

            assert c == approx(sparse_cosine_similarity(u, v))

    def test_cosine_threshold(self):
        mono = monopartite_projection(BIPARTITE, 'people', part='part', metric='cosine', threshold=0.3)

        assert set(mono.nodes) == PEOPLE_PART

        assert set(mono.edges) == set([('John', 'Lucy'), ('Mary', 'Lucy')])

        for _, _, c in mono.edges(data='weight'):
            assert c >= 0.3

    def test_jaccard(self):
        mono = monopartite_projection(BIPARTITE, 'people', part='part', metric='jaccard')

        assert set(mono.nodes) == PEOPLE_PART

        for u, v, c in mono.edges(data='weight'):
            u = to_vector(BIPARTITE, u)
            v = to_vector(BIPARTITE, v)

            assert c == approx(jaccard_similarity(u, v))

    def test_overlap(self):
        mono = monopartite_projection(BIPARTITE, 'people', part='part', metric='overlap')

        assert set(mono.nodes) == PEOPLE_PART

        assert mono['John']['Lucy']['weight'] == 1.0

        for u, v, c in mono.edges(data='weight'):
            u = to_vector(BIPARTITE, u)
            v = to_vector(BIPARTITE, v)

            assert c == approx(overlap_coefficient(u, v))
