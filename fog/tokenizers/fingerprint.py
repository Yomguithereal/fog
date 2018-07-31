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


def create_fingerprint_tokenizer(keep_digits=True, min_token_size=1,
                                 split=None, stopwords=None, squeeze=False):
    """
    Function returning a custom fingerprint tokenizer.

    Args:
        keep_digits (bool, optional): Whether to keep digits in fingerprint?
            Defaults to True.
        min_token_size (int, optional): Minimum token size. Defaults to 1.
        split (list, optional): List of token splitting characters.
        stopwords (iterable, optional): List of stopwords to filter.
        squeeze (bool, optional): Whether to squeeze the tokens or not.

    Returns:
        function: A custom tokenizer.

    """

    STOPWORDS_RE = None
    SPLIT_RE = None
    MIN_TOKEN_SIZE_RE = None

    if stopwords is not None:
        STOPWORDS_RE = re.compile(
            '(?:' + '|'.join(['\\b' + re.escape(s) + '\\b' for s in stopwords]) + ')',
            re.I
        )

    if split is not None:
        SPLIT_RE = re.compile('[' + re.escape(''.join(split)) + ']')

    if min_token_size and min_token_size > 1:
        MIN_TOKEN_SIZE_RE = re.compile('\\b\\S{1,%i}\\b' % min_token_size)

    def tokenizer(string):

        # Splitting
        if SPLIT_RE is not None:
            string = re.sub(SPLIT_RE, ' ', string)

        # Stopwords
        if STOPWORDS_RE is not None:
            string = re.sub(STOPWORDS_RE, '', string)

        # Digits
        if not keep_digits:
            string = re.sub(DIGITS_RE, '', string)

        # Case normalization
        string = string.lower()

        # Minimum token size
        if MIN_TOKEN_SIZE_RE:
            string = re.sub(MIN_TOKEN_SIZE_RE, '', string)

        # Deburring
        string = unidecode(string)

        # Only keeping letters
        string = re.sub(BLACKLIST_RE, '', string)

        # Trimming
        string = string.strip()

        # Squeezing
        if squeeze:
            string = squeeze_string(string)

        # Tokenizing
        tokens = re.split(WHITESPACE_RE, string)

        # Keeping unique tokens
        tokens = set(tokens)

        # Sorting
        tokens = sorted(tokens)

        return tokens

    return tokenizer


def create_ngrams_fingerprint_tokenizer(keep_digits=True, min_token_size=1,
                                        split=None, stopwords=None, squeeze=True):
    """
    Function returning a custom ngrams fingerprint tokenizer.

    Args:
        keep_digits (bool, optional): Whether to keep digits in fingerprint?
            Defaults to True.
        min_token_size (int, optional): Minimum token size. Defaults to 1.
        split (list, optional): List of token splitting characters.
        stopwords (iterable, optional): List of stopwords to filter.
        squeeze (bool, optional): Whether to squeeze the tokens or not.

    Returns:
        function: A custom tokenizer.

    """

    STOPWORDS_RE = None
    SPLIT_RE = None
    MIN_TOKEN_SIZE_RE = None

    if stopwords is not None:
        STOPWORDS_RE = re.compile(
            '(?:' + '|'.join(['\\b' + re.escape(s) + '\\b' for s in stopwords]) + ')',
            re.I
        )

    if split is not None:
        SPLIT_RE = re.compile('[' + re.escape(''.join(split)) + ']')

    if min_token_size and min_token_size > 1:
        MIN_TOKEN_SIZE_RE = re.compile('\\b\\S{1,%i}\\b' % min_token_size)

    def tokenizer(n, string):

        # Splitting
        if SPLIT_RE is not None:
            string = re.sub(SPLIT_RE, ' ', string)

        # Stopwords
        if STOPWORDS_RE is not None:
            string = re.sub(STOPWORDS_RE, '', string)

        # Digits
        if not keep_digits:
            string = re.sub(DIGITS_RE, '', string)

        # Case normalization
        string = string.lower()

        # Minimum token size
        if MIN_TOKEN_SIZE_RE:
            string = re.sub(MIN_TOKEN_SIZE_RE, '', string)

        # Deburring
        string = unidecode(string)

        # Only keeping letters
        string = re.sub(BLACKLIST_RE, '', string)

        # Trimming
        string = string.strip()

        # Squeezing
        if squeeze:
            string = squeeze_string(string)

        # Tokenizing
        string = re.sub(WHITESPACE_RE, '', string)
        tokens = ngrams(n, string)

        # Keeping unique tokens
        tokens = set(tokens)

        # Sorting
        tokens = sorted(tokens)

        return tokens

    return tokenizer


# Default fingerprint tokenizer
fingerprint_tokenizer = create_fingerprint_tokenizer()
ngrams_fingerprint_tokenizer = create_ngrams_fingerprint_tokenizer()
