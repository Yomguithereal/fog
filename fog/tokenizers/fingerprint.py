# =============================================================================
# Fog Fingerprint Tokenizers
# =============================================================================
#
# Functions for creating custom fingerprint tokenizers.
#
# Fingerprinting is a clever way to normalize strings in order to remove
# anything that would not compulsorily yield meaning such as token ordering,
# & duplication etc.
#
# The basic fingerprinting procedure is the following:
#   1. Normalizing the case
#   2. Normalizing unicode characters to plain ascii
#   3. Dropping any non-alphanumeric character
#   4. Dropping irrelevant whitespace
#   5. Tokenizing by splitting the string by whitespaces
#   6. Deduplicating the tokens
#   7. Sorting the tokens
#   8. Returning those tokens that will usually be re-joined by a single space
#
# For instance, this fingerprinting scheme will be able to match the
# following strings:
#   "University of North Carolina"
#   "North Carolina, university of"
#   "UNIVERSITY OF NORTH CAROLINA"
#   "University   of of north CarolINA"
#   "University --- of --- North Carolina"
#   "..."
#
# Optionally, one can chose more advanced and aggressive options such as
# filtering some tokens and squeezing the string etc.
#
# The ngram fingerprint is a variant that returns a list of normalized ngrams
# that will be joined in order rather than the whole tokens. It is
# sometimes useful to find misspelled strings.
#
# [Url]:
# http://openrefine.org/
#
import re
from unidecode import unidecode
from fog.utils import squeeze as squeeze_string
from fog.tokenizers.ngrams import ngrams

WHITESPACE_RE = re.compile('\\s+')
DIGITS_RE = re.compile('\\d+')
BLACKLIST_RE = re.compile('[^a-z0-9\\s]')


class FingerprintTokenizer(object):
    """
    Function returning a custom fingerprint tokenizer.

    Args:
        keep_digits (bool, optional): Whether to keep digits in fingerprint?
            Defaults to True.
        min_token_size (int, optional): Minimum token size. Defaults to 1.
        split (list, optional): List of token splitting characters.
        stopwords (iterable, optional): List of stopwords to filter.
        squeeze (bool, optional): Whether to squeeze the tokens or not.
    """

    def __init__(self, keep_digits=True, min_token_size=1,
                 split=None, stopwords=None, squeeze=False):

        self.keep_digits = keep_digits
        self.squeeze = squeeze

        self.stopwords_re = None
        self.split_re = None
        self.min_token_size_re = None

        if stopwords is not None:
            self.stopwords_re = re.compile(
                '(?:' + '|'.join(['\\b' + re.escape(s) + '\\b' for s in stopwords]) + ')',
                re.I
            )

        if split is not None:
            self.split_re = re.compile('[' + re.escape(''.join(split)) + ']')

        if min_token_size and min_token_size > 1:
            self.min_token_size_re = re.compile('\\b\\S{1,%i}\\b' % min_token_size)

    def tokenize(self, string):

        # Splitting
        if self.split_re is not None:
            string = re.sub(self.split_re, ' ', string)

        # Stopwords
        if self.stopwords_re is not None:
            string = re.sub(self.stopwords_re, '', string)

        # Digits
        if not self.keep_digits:
            string = re.sub(DIGITS_RE, '', string)

        # Case normalization
        string = string.lower()

        # Minimum token size
        if self.min_token_size_re:
            string = re.sub(self.min_token_size_re, '', string)

        # Deburring
        string = unidecode(string)

        # Only keeping letters
        string = re.sub(BLACKLIST_RE, '', string)

        # Trimming
        string = string.strip()

        # Squeezing
        if self.squeeze:
            string = squeeze_string(string)

        # Tokenizing
        tokens = re.split(WHITESPACE_RE, string)

        # Keeping unique tokens
        tokens = set(tokens)

        # Sorting
        tokens = sorted(tokens)

        return tokens

    def __call__(self, string):
        return self.tokenize(string)

    def key(self, string):
        return ' '.join(self.tokenize(string))


class NgramsFingerprintTokenizer(FingerprintTokenizer):
    def tokenize(self, n, string):

        # Splitting
        if self.split_re is not None:
            string = re.sub(self.split_re, ' ', string)

        # Stopwords
        if self.stopwords_re is not None:
            string = re.sub(self.stopwords_re, '', string)

        # Digits
        if not self.keep_digits:
            string = re.sub(DIGITS_RE, '', string)

        # Case normalization
        string = string.lower()

        # Minimum token size
        if self.min_token_size_re:
            string = re.sub(self.min_token_size_re, '', string)

        # Deburring
        string = unidecode(string)

        # Only keeping letters
        string = re.sub(BLACKLIST_RE, '', string)

        # Trimming
        string = string.strip()

        # Squeezing
        if self.squeeze:
            string = squeeze_string(string)

        # Tokenizing
        string = re.sub(WHITESPACE_RE, '', string)
        tokens = ngrams(n, string)

        # Keeping unique tokens
        tokens = set(tokens)

        # Sorting
        tokens = sorted(tokens)

        return tokens

    def __call__(self, n, string):
        return self.tokenize(n, string)

    def key(self, n, string):
        return ''.join(self.tokenize(n, string))
