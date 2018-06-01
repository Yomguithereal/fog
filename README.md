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
  - [jaccard_similarity](#jaccard_similarity)
  - [weighted_jaccard_similarity](#weighted_jaccard_similarity)

### Metrics

#### sparse_cosine_similarity

Computes the cosine similarity of two sparse weighted sets. Those sets have to be represented as counters.

```python
from fog.metrics import sparse_cosine_similarity

# Basic
sparse_cosine_similarity({'apple': 34, 'pear': 3}, {'pear': 1, 'orange': 1})
>>> ~0.062
```

*Arguments*

* **A** *Counter*: first weighted set. Must be a dictionary mapping keys to weights.
* **B** *Counter*: second weighted set. Muset be a dictionary mapping keys to weights.

---

#### jaccard_similarity

Computes the Jaccard similarity of two arbitrary iterables.

```python
from fog.metrics import jaccard_similarity

# Basic
jaccard_similarity('context', 'contact')
>>> ~0.571
```

*Arguments*

* **A** *iterable*: first sequence to compare.
* **B** *iterable*: second sequence to compare.

---

#### weighted_jaccard_similarity

Computes the weighted Jaccard similarity of two weighted sets. Those sets have to be represented as counters.

```python
from fog.metrics import weighted_jaccard_similarity

# Basic
weighted_jaccard_similarity({'apple': 34, 'pear': 3}, {'pear': 1, 'orange': 1})
>>> ~0.026
```

*Arguments*

* **A** *Counter*: first weighted set. Must be a dictionary mapping keys to weights.
* **B** *Counter*: second weighted set. Muset be a dictionary mapping keys to weights.
