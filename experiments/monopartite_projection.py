import csv
import networkx as nx
from fog.graph import cosine_monopartite_projection
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
    monopartite = cosine_monopartite_projection(bipartite, 'account', part='node_type')

print(monopartite.order(), monopartite.size())

nx.write_gexf(monopartite, './output/monopartite.gexf')
