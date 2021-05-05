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

ENGLISH_CONTRACTIONS = ['ll', 're', 'm', 's', 've', 'd']
FRENCH_EXCEPTIONS = ['hui']

# TODO: exceptions, abbreviations, urls, mails, negatives, chomping junk mid word? smileys?
# TODO: trailing point number, drop lang to support all contractions
# TODO: O' 'Nguyen l' arrivee, l'herbe, is n't (check treebank)
# TODO: consuming functions?

# D'mitr,Dimitri
# N'Guyen,Nguyen
# O'Doherty,Dougherty
# O'Hara,Ohara
# 'Mbappé,Mbappe
# 'Mbappe,Mbappe
# M'bappé,Mbappe
# M'Leod,MacLeod
# Ibn al' rasheed,Rasheed
# Ibn' al'rasheed,Rasheed
# Rourke,O 'Rourke
# O'Rourke,O'Rourke
# O Rourke,O'Rourke
# N'diaye,Ndiaye
# 'Ndiaye,Ndiaye
# Lochlann',Laughlin
# N'Djaména,Ndjamena
# N'Djamena,Ndjamena
# 'Aamir,Aamir
# D'Encausse,D'Encausse
# D'encausse,D'Encausse
# Dencausse,D'Encausse
# DEncausse,D'Encausse
# L'Arrivée,Larrivée
# Han'gŭl,Hangul


def is_ascii_junk(c):
    return ord(c) <= 0x1F


def is_ascii_alpha(c):
    return bool(ASCII_ALPHA_PATTERN.match(c))


def is_valid_twitter_char(c):
    return bool(TWITTER_CHAR_PATTERN.match(c))


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
            if j > i and j < l and string[j] in APOSTROPHES:
                before = string[i:j]

                k = j + 1

                while k < l:
                    if not string[k].isalpha():
                        break

                    k += 1

                if k > j:
                    after = string[j + 1:k]

                    if after in ENGLISH_CONTRACTIONS:
                        yield before
                        yield string[j] + after

                    elif (
                        (before.endswith('n') and after == 't') or
                        after in FRENCH_EXCEPTIONS
                    ):
                        yield string[i:k]

                    else:
                        yield before + string[j]
                        i = j + 1
                        continue

                else:
                    yield before

                j = k

            elif j > i:
                yield string[i:j]

            i = j

    def __call__(self, string):
        return self.tokenize(string)
