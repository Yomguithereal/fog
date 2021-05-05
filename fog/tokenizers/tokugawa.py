# =============================================================================
# Fog Tokugawa Tokenizer
# =============================================================================
#
# A general purpose word tokenizer.
#

DECIMALS = '.,'
APOSTROPHES = '\'’'


class TokugawaTokenizer(object):
    def __init__(self, *, lang='en'):
        self.lang = lang

    def __call__(self, string):
        tokens = []

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
                tokens.append(c)
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

            if j > i + 1:
                tokens.append(string[i:j])

            i = j

        return tokens
