[![Build Status](https://travis-ci.org/Yomguithereal/fog.svg)](https://travis-ci.org/Yomguithereal/fog)

# Fog

A fuzzy matching/clustering library for Python.

## Installation

You can install `fog` with pip with the following command:

```
pip install fog
```

## Usage

* [Metrics](#metrics)
  - [sparse_cosine_similarity](#sparse_cosine_similarity)
  - [weighted_jaccard_similarity](#weighted_jaccard_similarity)

### Metrics

#### sparse_cosine_similarity

Computes the cosine similarity of two sparse weighted sets. Those sets have to be represented as counters.

```python
from fog.metrics import sparse_cosine_similarity

# Basic
sparse_cosine_similarity({'apple': 34, 'pear': 3}, {'pear': 1, 'orange': 1})
>>> ~0.062

# Using custom key
A = {'apple': {'weight': 34}, 'pear': {'weight': 3}}
B = {'pear': {'weight': 1}, 'orange': {'weight': 1}}
sparse_cosine_similarity(A, B, key=lambda x: x['weight'])
```

*Arguments*

* **A** *Counter*: first weighted set. Must be a dictionary mapping keys to weights.
* **B** *Counter*: second weighted set. Muset be a dictionary mapping keys to weights.
* **key** *?callable*: Optional function retrieving the weight from values.

#### weighted_jaccard_similarity

Computes the weighted Jaccard similarity of two weighted sets. Those sets have to be represented as counters.

```python
from fog.metrics import weighted_jaccard_similarity

# Basic
weighted_jaccard_similarity({'apple': 34, 'pear': 3}, {'pear': 1, 'orange': 1})
>>> ~0.026

# Using custom key
A = {'apple': {'weight': 34}, 'pear': {'weight': 3}}
B = {'pear': {'weight': 1}, 'orange': {'weight': 1}}
weighted_jaccard_similarity(A, B, key=lambda x: x['weight'])
```

*Arguments*

* **A** *Counter*: first weighted set. Must be a dictionary mapping keys to weights.
* **B** *Counter*: second weighted set. Muset be a dictionary mapping keys to weights.
* **key** *?callable*: Optional function retrieving the weight from values.
