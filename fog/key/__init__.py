from fog.key.fingerprint import (
    FingerprintingKeyer,
    NgramsFingerprintKeyer
)
from fog.key.levenshtein import (
    levenshtein_1d_keys,
    damerau_levenshtein_1d_keys,
    levenshtein_1d_blocks,
    damerau_levenshtein_1d_blocks,
    levenshtein_2d_blocks,
    damerau_levenshtein_2d_blocks
)
from fog.key.misc import ngram_keys, zig_zag
from fog.key.omission import omission_key
from fog.key.skeleton import skeleton_key

fingerprint = FingerprintingKeyer()
ngrams_fingerprint = NgramsFingerprintKeyer()
