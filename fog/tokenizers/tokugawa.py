# =============================================================================
# Fog Tokugawa Tokenizer
# =============================================================================
#
# A general purpose word tokenizer.
#
import re

DECIMALS = '.,'
APOSTROPHES = '\'’'
ASCII_ALPHA_PATTERN = re.compile(r'^[A-Za-z]$')
TWITTER_CHAR_PATTERN = re.compile(r'^[A-Za-z0-9_]$')

# TODO: exceptions, abbreviations, urls, mails, negatives, chomping junk mid word? smileys?


def is_ascii_junk(c):
    return ord(c) <= 0x1F


def is_ascii_alpha(c):
    return bool(ASCII_ALPHA_PATTERN.match(c))


def is_valid_twitter_char(c):
    return bool(TWITTER_CHAR_PATTERN.match(c))


class TokugawaTokenizer(object):
    def __init__(self, *, lang='en', mentions=True, hashtags=True):
        self.lang = lang
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
                while (
                    j < l and
                    not c.isspace() and
                    (string[j].isdigit() or string[j] in DECIMALS)
                ):
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

            # Handling contractions
            if j < l and self.lang != 'en' and string[j] in APOSTROPHES:
                j += 1

            if j > i:
                yield string[i:j]

            i = j

    def __call__(self, string):
        return self.tokenize(string)
