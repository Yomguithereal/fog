from fog.tokenizers.fingerprint import (
    FingerprintTokenizer,
    NgramsFingerprintTokenizer
)
from fog.tokenizers.ngrams import ngrams, bigrams, trigrams, quadrigrams
from fog.tokenizers.words import WordTokenizer

fingerprint_tokenizer = FingerprintTokenizer()
ngrams_fingerprint_tokenizer = NgramsFingerprintTokenizer()
words_tokenizer = WordTokenizer()
