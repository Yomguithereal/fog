import csv
import networkx as nx
from fog.graph import monopartite_projection, floatsam_sparsification
from experiments.utils import Timer

bipartite = nx.Graph()

with open('./data/bipartite.csv') as f:
    reader = csv.DictReader(f)

    for line in reader:
        account = 'a%s' %line['account']
        url = 'u%s' % line['url']

        bipartite.add_node(account, node_type='account')
        bipartite.add_node(url, node_type='url')
        bipartite.add_edge(account, url, weight=int(line['weight']))

with Timer('quadratic'):
    monopartite = monopartite_projection(bipartite, 'account',
        part='node_type',
        metric='cosine',
        threshold=0.1,
        bipartition_check=False,
        use_topology=False
    )

print(monopartite.order(), monopartite.size())

with Timer('index'):
    monopartite = monopartite_projection(bipartite, 'account',
        part='node_type',
        metric='cosine',
        threshold=0.1,
        bipartition_check=False
    )

print(monopartite.order(), monopartite.size())

nx.write_gexf(monopartite, './output/monopartite.gexf')

with Timer('floatsam'):
    best_threshold = floatsam_sparsification(monopartite, 0.3, learning_rate=0.01, remove_edges=True)

print(monopartite.order(), monopartite.size(), best_threshold)

nx.write_gexf(monopartite, './output/sparse.gexf')
