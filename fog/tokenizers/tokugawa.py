# =============================================================================
# Fog Tokugawa Tokenizer
# =============================================================================
#
# A general purpose word tokenizer.
#

DECIMALS = '.,'
APOSTROPHES = '\'’'

# TODO: ascii junk, tabs, squeeze, exceptions, abbreviations, acronyms, hashtags, mentions, urls


class TokugawaTokenizer(object):
    def __init__(self, *, lang='en'):
        self.lang = lang

    def __call__(self, string):
        i = 0
        l = len(string)

        while i < l:
            c = string[i]

            # Chomping spaces
            if c.isspace():
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
                while (
                    j < l and
                    not string[j].isspace() and
                    string[j].isalnum()
                ):
                    j += 1

            # Handling contractions
            if self.lang != 'en' and string[j] in APOSTROPHES:
                j += 1

            if j > i:
                yield string[i:j]

            i = j
