[![Build Status](https://travis-ci.org/Yomguithereal/fog.svg)](https://travis-ci.org/Yomguithereal/fog)

# Fog

A fuzzy matching/clustering library for Python.

## Installation

You can install `fog` with pip with the following command:

```
pip install fog
```

## Usage

* [Graph](#graph)
  * [monopartite_projection](#monopartite_projection)
* [Metrics](#metrics)
  * [jaccard_similarity](#jaccard_similarity)
  * [sparse_cosine_similarity](#sparse_cosine_similarity)
  * [weighted_jaccard_similarity](#weighted_jaccard_similarity)

### Graph

#### monopartite_projection

Function computing a monopartite projection of the given bipartite graph.
This projection can be basic and create a weighted edge each time two nodes
in target partition share a common neighbor. Or it can be weighted and
filtered using a similarity metric such as Jaccard or cosine similarity,
for instance.

*Arguments*
* **bipartite** *nx.Graph*: Target bipartite graph.
* **project** *str*: Name of the partition to project.
* **part** *?str* [`bipartite`]: Name of the node attribute on which the
graph partition is built e.g. "color" or "type" etc.
* **weight** *?str* [`weight`]: Name of the weight edge attribute.
* **metric** *?str* [`None`]: Metric to use. If `None`, the basic projection
will be returned. Also accepts `jaccard`, `overlap` or `cosine`.
* **threshold** *?float* [`None`]: Optional similarity threshold under which
edges won't be added to the monopartite projection.
* **use_topology** *?bool*: Whether to use the bipartite graph's
topology to attempt a subquadratic time projection. Intuitively,
this works by not computing similarities of all pairs of nodes but
only of pairs of nodes that share at least a common neighbor.
It generally works better than the quadratic approach but can
sometimes hurt your performance by losing time on graph traversals
when your graph is very dense.
* **bipartition_check** *?bool*: This function will start by checking
whether your graph is bipartite because it can get stuck in an
infinite loop if given graph is not truly bipartite. Be sure to
disable this kwarg if you know beforehand that your graph is
bipartite and for better performance.

### Metrics

#### jaccard_similarity

Function computing the Jaccard similarity. That is to say the intersection
of input sets divided by their union.

Runs in O(n), n being the size of the smallest set.

```python
from fog.metrics import jaccard_similarity

# Basic
jaccard_similarity('context', 'contact')
>>> ~0.571
```

*Arguments*
* **A** *iterable*: First sequence.
* **B** *iterable*: Second sequence.

#### sparse_cosine_similarity

Function computing cosine similarity on sparse weighted sets represented
by python dicts.

Runs in O(n), n being the sum of A & B's sizes.

```python
from fog.metrics import sparse_cosine_similarity

# Basic
sparse_cosine_similarity({'apple': 34, 'pear': 3}, {'pear': 1, 'orange': 1})
>>> ~0.062
```

*Arguments*
* **A** *Counter*: First weighted set.
* **B** *Counter*: Second weighted set.

#### weighted_jaccard_similarity

Function computing the weighted Jaccard similarity.
Runs in O(n), n being the sum of A & B's sizes.

```python
from fog.metrics import weighted_jaccard_similarity

# Basic
weighted_jaccard_similarity({'apple': 34, 'pear': 3}, {'pear': 1, 'orange': 1})
>>> ~0.026
```

*Arguments*
* **A** *Counter*: First weighted set.
* **B** *Counter*: Second weighted set.
