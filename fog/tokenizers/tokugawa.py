# =============================================================================
# Fog Tokugawa Tokenizer
# =============================================================================
#
# A general purpose word tokenizer.
#
import re

DECIMALS = ['.', ',']
APOSTROPHES = ['\'', '’']
IRISH = ['O', 'o']
ASCII_ALPHA_RE = re.compile(r'^[A-Za-z]$')
TWITTER_CHAR_RE = re.compile(r'^[A-Za-z0-9_]$')
VOWELS_PATTERN = 'aáàâäąåoôóøeéèëêęiíïîıuúùûüyÿæœAÁÀÂÄĄÅOÓÔØEÉÈËÊĘIİÍÏÎYŸUÚÙÛÜÆŒ'
VOWELS_RE = re.compile(r'^[%s]$' % VOWELS_PATTERN)
CONSONANTS_RE = re.compile(r'^[^%s]$' % VOWELS_PATTERN)

ENGLISH_CONTRACTIONS = ['ll', 're', 'm', 's', 've', 'd']
FRENCH_EXCEPTIONS = ['hui']
ABBREVIATIONS = {
    'dr',
    'etc',
    'jr',
    'm',
    'mgr',
    'mr',
    'mrs',
    'ms',
    'mme',
    'mlle',
    'prof',
    'sr',
    'st',
    'p',
    'pp'
}

# TODO: urls, mails, negatives, chomping junk mid word? smileys?
# TODO: tagged tokens
# TODO: what about lists: 1), 1, etc.


def is_ascii_junk(c):
    return ord(c) <= 0x1F


def is_ascii_alpha(c):
    return bool(ASCII_ALPHA_RE.match(c))


def is_valid_twitter_char(c):
    return bool(TWITTER_CHAR_RE.match(c))


def is_vowel(c):
    return bool(VOWELS_RE.match(c))


def is_consonant(c):
    return bool(CONSONANTS_RE.match(c))


def string_get(string, i):
    try:
        return string[i]
    except IndexError:
        return None


class TokugawaTokenizer(object):
    def __init__(self, *, mentions=True, hashtags=True):
        self.mentions = mentions
        self.hashtags = hashtags

    def tokenize(self, string):
        i = 0
        l = len(string)

        while i < l:
            c = string[i]

            # Chomping spaces and ASCII junk
            if c.isspace() or is_ascii_junk(c):
                i += 1
                continue

            can_be_mention = self.mentions and c == '@'
            can_be_hashtag = self.hashtags and (c == '#' or c == '$')

            # Guarding some cases
            if can_be_mention or can_be_hashtag:
                pass

            # Breaking punctuation apart
            elif not c.isalnum() and c not in APOSTROPHES:

                # Surrogates
                while i + 1 < l and string[i + 1] == '\u200d':
                    c += string[i + 1:i + 3]
                    i += 2

                yield c
                i += 1
                continue

            # Consuming token
            j = i + 1

            if can_be_hashtag and not is_ascii_alpha(string[j]):
                yield c
                i += 1
                continue

            # Mention and hashtag token
            if can_be_mention or can_be_hashtag:
                while j < l and is_valid_twitter_char(string[j]):
                    j += 1

            # Numerical token
            elif c.isdigit():
                digit_separator = None

                while j < l:
                    if c.isspace():
                        break

                    if string[j] in DECIMALS:
                        if digit_separator is not None:
                            if string[j] != digit_separator:
                                break
                        else:
                            digit_separator = string[j]

                        j += 1
                        continue

                    if not string[j].isdigit():
                        break

                    j += 1

            # Alphanumerical token
            else:
                while j < l:
                    if string[j].isspace():
                        break

                    if not string[j].isalnum():
                        if string[j] == '.' and string[j - 1].isupper():
                            j += 1
                            continue

                        break

                    j += 1

            before = string[i:j]

            # Handling contractions
            if j < l and string[j] in APOSTROPHES:
                k = j + 1

                while k < l:
                    if not string[k].isalpha():
                        break

                    k += 1

                if k > j + 1:
                    after = string[j + 1:k]

                    if after in ENGLISH_CONTRACTIONS:
                        yield before
                        yield string[j] + after

                    elif (
                        (before.endswith('n') and after == 't') or
                        after in FRENCH_EXCEPTIONS
                    ):
                        yield string[i:k]

                    # NOTE: maybe this condition needs to check before is one letter long and an uppercase letter?
                    elif (
                        (
                            is_consonant(before[-1]) and
                            (
                                (after[0].isupper() and string_get(string, k) != '.') or
                                (is_consonant(after[0]) and after[0] != 'h')
                            )
                        ) or
                        before in IRISH
                    ):
                        yield before + string[j] + after

                    else:
                        yield before + string[j]
                        i = j + 1
                        continue

                else:
                    yield before

                j = k

            # Handling abbreviations
            elif j < l - 1 and string[j] == '.' and before.lower() in ABBREVIATIONS:
                yield before + '.'
                j += 1

            # Handling regular word
            else:
                yield before

            i = j

    def __call__(self, string):
        return self.tokenize(string)
