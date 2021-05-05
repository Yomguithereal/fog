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
URL_START_RE = re.compile(r'^https?://')

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

# TODO: mails, chomping junk mid word? smileys?
# TODO: tagged tokens


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


def starts_as_url(string, i):
    return bool(URL_START_RE.match(string[i:i + 8]))


def string_get(string, i):
    try:
        return string[i]
    except IndexError:
        return None


class TokugawaTokenizer(object):
    def tokenize(self, string):
        i = 0
        l = len(string)

        while i < l:
            c = string[i]

            # Chomping spaces and ASCII junk
            if c.isspace() or is_ascii_junk(c):
                i += 1
                continue

            can_be_mention = c == '@'
            can_be_hashtag = (c == '#' or c == '$')

            # Guarding some cases
            if can_be_mention or can_be_hashtag:
                pass

            # Breaking punctuation apart
            elif not c.isalnum() and c not in APOSTROPHES and c != '-':

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
            elif c.isdigit() or c == '-':
                while j < l:
                    if c.isspace():
                        break

                    if not string[j].isdigit() and string[j] not in DECIMALS:
                        break

                    j += 1

                if j > i + 1 and string[j - 1] in DECIMALS:
                    j -= 1

            # Alphanumerical token
            else:
                could_be_url = starts_as_url(string, i)

                while j < l:
                    if string[j].isspace():
                        break

                    if not could_be_url and not string[j].isalnum():
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
