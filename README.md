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
  * [floatsam_sparsification](#floatsam_sparsification)
  * [monopartite_projection](#monopartite_projection)
* [Metrics](#metrics)
  * [cosine_similarity](#cosine_similarity)
  * [sparse_cosine_similarity](#sparse_cosine_similarity)
  * [sparse_dot_product](#sparse_dot_product)
  * [jaccard_similarity](#jaccard_similarity)
  * [weighted_jaccard_similarity](#weighted_jaccard_similarity)
  * [overlap_coefficient](#overlap_coefficient)

### Graph

#### floatsam_sparsification

Function using an iterative algorithm to try and find the best weight
threshold to apply to trim the given graph's edges while keeping the
underlying community structures.

It works by iteratively increasing the threshold and stopping as soon as
a significant connected component starts to drift away from the principal
one.

This is basically a very naive gradient descent with a very naive cost
function but it works decently for typical cases.

*Arguments*
* **graph** *nx.Graph*: Graph to sparsify.
* **starting_treshold** *float*: Starting similarity threshold.
* **learning_rate** *?float* [`0.05`]: How much to increase the threshold
at each step of the algorithm.
* **max_drifter_size** *?int*: Max size of component to detach itself
from the principal one before stopping the algorithm. If not
provided it will default to the logarithm of the graph's total
number of nodes.
* **weight** *?str* [`weight wrt networkx conventions`]: Name of the weight attribute.
* **remove_edges** *?bool* [`False`]: Whether to remove edges from the graph
having a weight less than found threshold or not. Note that if
`True`, this will mutate the given graph.

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

#### cosine_similarity

Function computing the cosine similarity of the given sequences.
Runs in O(n), n being the sum of A & B's sizes.

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

#### sparse_dot_product

Function used to compute the dotproduct of sparse weighted sets represented
by python dicts.

Runs in O(n), n being the size of the smallest set.

*Arguments*
* **A** *Counter*: First weighted set.
* **B** *Counter*: Second weighted set.

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

#### overlap_coefficient

Function computing the overlap coefficient of the given sets, i.e. the size
of their intersection divided by the size of the smallest set.

Runs in O(n), n being the size of the smallest set.

*Arguments*
* **A** *iterable*: First sequence.
* **B** *iterable*: Second sequence.
