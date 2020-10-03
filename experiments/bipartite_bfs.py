import networkx as nx
from collections import deque

NODES = [
    ('John', 'people'),
    ('Mary', 'people'),
    ('Lucy', 'people'),
    ('Gabriel', 'people'),
    ('Meredith', 'people'),
    ('Marc', 'people'),
    ('Anna', 'people'),
    ('red', 'color'),
    ('blue', 'color'),
    ('yellow', 'color'),
    ('purple', 'color'),
    ('orange', 'color'),
    ('cyan', 'color'),
    ('magenta', 'color'),
    ('green', 'color'),
]

EDGES = [
    ('John', 'red', 1.0),
    ('John', 'purple', 3.0),
    ('Gabriel', 'yellow', 2.0),
    ('Gabriel', 'orange', 4.0),
    ('Mary', 'red', 2.0),
    ('Mary', 'yellow', 1.0),
    ('Lucy', 'red', 7.0),
    ('Lucy', 'purple', 1.0),
    ('Marc', 'purple', 0.5),
    ('Mary', 'magenta', 4.5),
    ('John', 'magenta', 1.0),
    ('John', 'cyan', 2.0),
    ('Anna', 'green', 1.0),
    ('Anna', 'orange', 6.5),
    ('Gabriel', 'green', 1.0),
    ('Marc', 'yellow', 0.1),
]

bipartite = nx.Graph()

for key, part in NODES:
    bipartite.add_node(key, part=part)

bipartite.add_weighted_edges_from(EDGES)

def bfs(g, data=None, default=None):
    seen = set()
    q = deque()

    def component_generator():
        while len(q) != 0:
            p, n1 = q.popleft()

            if data is None:
                yield p, n1
            else:
                attr = g.nodes[n1]
                attr = attr if data is True else attr.get(data, default)

                yield p, n1, attr

            for i, n2 in enumerate(g.neighbors(n1)):
                if n2 in seen:
                    continue

                seen.add(n2)
                q.append((p + [(i, n1)], n2))

    for node in g.nodes:
        if node in seen:
            continue

        q.append(([], node))
        seen.add(node)

        yield component_generator()

for component in bfs(bipartite, data='part'):
    component = list(component)

    for p, node, part in component:
        # if part == 'color':
        #     continue
        print(node.ljust(8), ' - ', str(len(p)) + '::' + str(tuple(p)))

    # print('Path:: ', ' -> '.join(n for _, n, _ in component))
    print()
