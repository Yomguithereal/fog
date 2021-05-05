# =============================================================================
# Fog Tokugawa Tokenizer
# =============================================================================
#
# A general purpose word tokenizer.
#

DECIMALS = '.,'
APOSTROPHES = '\'’'

# TODO: exceptions, abbreviations, hashtags, mentions, urls


def is_ascii_junk(c):
    return ord(c) <= 0x1F


class TokugawaTokenizer(object):
    def __init__(self, *, lang='en'):
        self.lang = lang

    def tokenize(self, string):
        i = 0
        l = len(string)

        while i < l:
            c = string[i]

            # Chomping spaces and ASCII junk
            if c.isspace() or is_ascii_junk(c):
                i += 1
                continue

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

            # Numerical token
            if c.isdigit():
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
