# =============================================================================
# Fog Fingerprint
# =============================================================================
#
# Functions returning string fingerprints.
#
from fog.tokenizers.fingerprint import (
    FingerprintTokenizer,
    NgramsFingerprintTokenizer
)


class FingerprintingKeyer(FingerprintTokenizer):
    def __call__(self, string):
        return self.key(string)


class NgramsFingerprintKeyer(NgramsFingerprintTokenizer):
    def __call__(self, n, string):
        return self.key(n, string)
