import csv
import networkx as nx
from fog.graph import monopartite_projection
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
        threshold=0.3
    )

print(monopartite.order(), monopartite.size())

with Timer('index'):
    monopartite = monopartite_projection(bipartite, 'account',
        part='node_type',
        metric='cosine',
        threshold=0.3,
        use_index=True
    )

print(monopartite.order(), monopartite.size())

nx.write_gexf(monopartite, './output/monopartite.gexf')
