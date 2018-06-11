# =============================================================================
# Fog Fingerprint
# =============================================================================
#
# Functions returning string fingerprints.
#
from fog.tokenizers.fingerprint import (
    create_fingerprint_tokenizer,
    create_ngrams_fingerprint_tokenizer
)


def create_fingerprint(**kwargs):
    tokenizer = create_fingerprint_tokenizer(**kwargs)

    def fingerprint_key(string):
        return ' '.join(tokenizer(string))

    return fingerprint_key


def create_ngrams_fingerprint(**kwargs):
    tokenizer = create_ngrams_fingerprint_tokenizer(**kwargs)

    def ngrams_fingerprint_key(n, string):
        return ''.join(tokenizer(n, string))

    return ngrams_fingerprint_key


# Defaults
fingerprint = create_fingerprint()
ngrams_fingerprint = create_ngrams_fingerprint()
