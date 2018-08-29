from fog.metrics.cosine import (
    cosine_similarity,
    sparse_cosine_similarity,
    sparse_dot_product
)
from fog.metrics.jaccard import (
    jaccard_similarity,
    weighted_jaccard_similarity
)
from fog.metrics.levenshtein import (
    levenshtein_distance,
    limited_levenshtein_distance,
    levenshtein_distance_lte1,
    damerau_levenshtein_distance_lte1
)
from fog.metrics.overlap import overlap_coefficient
