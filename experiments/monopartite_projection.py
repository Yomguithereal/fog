import csv
from networkx import Graph
from fog.graph import cosine_monopartite_projection

bipartite = Graph()

with open('./data/bipartite.csv') as f:
    reader = csv.DictReader(f)

    for line in reader:
        account = 'a%s' %line['account']
        url = 'u%s' % line['url']

        bipartite.add_node(account, type='account')
        bipartite.add_node(url, type='url')
        bipartite.add_edge(account, url, weight=int(line['weight']))

monopartite = cosine_monopartite_projection(bipartite, 'account', part='type')
