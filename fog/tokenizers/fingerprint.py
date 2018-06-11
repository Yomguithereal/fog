# =============================================================================
# Fog Fingerprint Tokenizers
# =============================================================================
#
# Functions for creating custom fingerprint tokenizers.
#
import re
from unidecode import unidecode
from fog.tokenizers.ngrams import ngrams

# TODO: better docs
WHITESPACE_RE = re.compile('\\s+')
DIGITS_RE = re.compile('\\d+')
PUNCTUATION_CONTROL_RE = re.compile('[\\u2000-\\u206F\\u2E00-\\u2E7F\'!"#$%&()*+,\\-.\\/:;<=>?@\\[\\]^_`{|}~\\x00-\\x08\\x0A-\\x1F\\x7F]')


def create_fingerprint_tokenizer(keep_digits=True, min_token_size=1,
                                 split=None, stopwords=None):
    """
    Function returning a custom fingerprint tokenizer.

    Args:
        keep_digits (bool, optional): Whether to keep digits in fingerprint?
            Defaults to True.
        min_token_size (int, optional): Minimum token size. Defaults to 1.
        split (list, optional): List of token splitting characters.
        stopwords (iterable, optional): List of stopwords to filter.

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

        # Dropping punctuation & control characters
        string = re.sub(PUNCTUATION_CONTROL_RE, '', string)

        # Deburring
        string = unidecode(string)

        # Trimming
        string = string.strip()

        # Tokenizing
        tokens = re.split(WHITESPACE_RE, string)

        # Keeping unique tokens
        tokens = set(tokens)

        # Sorting
        tokens = sorted(tokens)

        return tokens

    return tokenizer


def create_ngrams_fingerprint_tokenizer(keep_digits=True, min_token_size=1,
                                        split=None, stopwords=None):
    """
    Function returning a custom ngrams fingerprint tokenizer.

    Args:
        keep_digits (bool, optional): Whether to keep digits in fingerprint?
            Defaults to True.
        min_token_size (int, optional): Minimum token size. Defaults to 1.
        split (list, optional): List of token splitting characters.
        stopwords (iterable, optional): List of stopwords to filter.

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

        # Dropping punctuation & control characters
        string = re.sub(PUNCTUATION_CONTROL_RE, '', string)

        # Deburring
        string = unidecode(string)

        # Trimming
        string = string.strip()

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
