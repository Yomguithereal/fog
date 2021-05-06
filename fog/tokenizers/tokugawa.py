# =============================================================================
# Fog Tokugawa Tokenizer
# =============================================================================
#
# A general purpose word tokenizer able to consider a lot of edge case and
# typical entities all while remaining mostly language agnostic when working on
# languages separating its word token using whitespace (not the asian languages,
# for instance).
#
# The resulting token streams are tagged by entity types (not part-of-speech).
#
# Some design choices:
#  * We chose to parse and tag as numbers only strings that could be parsed
#    as such without ambiguity. This means word tokens may contain things that
#    could be considered as numbers, but you can parse them down the line.
#
# Here is a list of things we don't handle (yet):
#   * Complex graphemes such as: u̲n̲d̲e̲r̲l̲i̲n̲e̲d̲ or ārrive
#   * Multi-line hyphenation schemes
#   * Junk found in the middle of a word token
#
import re
from emoji import get_emoji_regexp
from ebbe import with_next

DECIMALS = ['.', ',']
APOSTROPHES = ['\'', '’']
IRISH = ['O', 'o']
TWITTER_CHAR_RE = re.compile(r'^[A-Za-z0-9_]$')
VOWELS_PATTERN = 'aáàâäąåoôóøeéèëêęiíïîıuúùûüyÿæœAÁÀÂÄĄÅOÓÔØEÉÈËÊĘIİÍÏÎYŸUÚÙÛÜÆŒ'
CONSONANTS_RE = re.compile(r'^[^%s]$' % VOWELS_PATTERN)
URL_START_RE = re.compile(r'^https?://')
EMAIL_LOOKAHEAD_RE = re.compile(r'^[A-Za-z0-9!#$%&*+\-/=?^_`{|}~]{1,64}@')
SMILEY_RE = re.compile(r'^(?:[\-]+>|<[\-]+|[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP/\:\}\{@\|\\]|[\)\]\(\[dDpP/\:\}\{@\|\\][\-o\*\']?[:;=8]|[<:]3)')
EMOJI_RE = get_emoji_regexp()
POINT_SPLITTER_RE = re.compile(r'(\.)')

ENGLISH_CONTRACTIONS = ['ll', 're', 'm', 's', 've', 'd']
FRENCH_EXCEPTIONS = ['hui']
ABBREVIATIONS = {
    'apt',
    'appt',
    'dr',
    'etc',
    'jr',
    'm',
    'mgr',
    'min',
    'mr',
    'mrs',
    'ms',
    'mme',
    'mlle',
    'no',
    'p',
    'pp',
    'prof',
    'sr',
    'st',
    'vs'
}


def is_ascii_junk(c):
    return ord(c) <= 0x1F


def is_valid_twitter_char(c):
    return bool(TWITTER_CHAR_RE.match(c))


def is_consonant(c):
    return bool(CONSONANTS_RE.match(c))


def starts_as_url(string, i):
    return bool(URL_START_RE.match(string[i:i + 8]))


def email_lookahead(string, i):
    return bool(EMAIL_LOOKAHEAD_RE.match(string[i:i + 64]))


def string_get(string, i):
    try:
        return string[i]
    except IndexError:
        return None


def with_holes(gen, string):
    last_index = 0

    for m in gen:
        if m.start() > last_index:
            for i in range(last_index, m.start()):
                yield ('punct', string[i])

        yield ('emoji', m.group(0))
        last_index = m.end()

    if last_index < len(string):
        for i in range(last_index, len(string)):
            yield ('punct', string[i])


def punct_emoji_iter(string):
    skip_next = False

    for item, next_item in with_next(with_holes(EMOJI_RE.finditer(string), string)):
        if skip_next:
            skip_next = False
            continue

        # Emoji combinator
        if next_item is not None and next_item[0] == 'punct' and ord(next_item[1]) == 65039:
            skip_next = True
            yield ('emoji', item[1] + next_item[1])

        else:
            yield item


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

            lookahead = string[i:i + 8]

            # Smileys?
            m = SMILEY_RE.match(lookahead)

            if m is not None:
                yield ('smiley', string[i:i + m.end()])
                i += m.end()
                continue

            # Guarding some cases
            if can_be_mention or can_be_hashtag:
                pass

            # Breaking punctuation apart and tokenizing emojis
            elif not c.isalnum() and c not in APOSTROPHES and c != '-':
                i += 1

                while i < l:
                    n = string[i]

                    if (
                        n.isspace() or
                        n.isalnum() or
                        is_ascii_junk(n) or
                        n == '#' or
                        n == '@'
                    ):
                        break

                    c += n
                    i += 1

                yield from punct_emoji_iter(c)

                continue

            # Consuming token
            j = i + 1
            token_type = 'word'
            already_consumed = False

            # Hashtags
            if can_be_hashtag:
                if j >= l or not string[j].isalpha():
                    yield ('punct', c)

                    i += 1
                    continue

                token_type = 'hashtag'

                while j < l and string[j].isalnum():
                    j += 1

                already_consumed = True

            # Mentions
            elif can_be_mention:
                if j >= l or not is_valid_twitter_char(string[j]):
                    yield ('punct', c)

                    i += 1
                    continue

                token_type = 'mention'

                while j < l and is_valid_twitter_char(string[j]):
                    j += 1

                already_consumed = True

            # Numerical token
            elif c.isdigit() or c == '-':
                already_consumed = True
                token_type = 'punct'
                last_char = c
                chosen_decimal = None

                while j < l:
                    if string[j].isspace():
                        break

                    if not string[j].isdigit():
                        if last_char in DECIMALS:
                            j -= 1
                            break

                        if (
                            last_char != '-' and
                            (
                                string[j].isalpha() or
                                string[j] == '-' or
                                string[j] == '_'
                            )
                        ):
                            already_consumed = False
                            token_type = 'word'
                            break

                        elif string[j] not in DECIMALS:
                            break

                        elif chosen_decimal is not None:
                            break

                        else:
                            chosen_decimal = string[j]

                    last_char = string[j]
                    token_type = 'number'
                    j += 1

                if already_consumed and j > i + 1 and string[j - 1] in DECIMALS:
                    j -= 1

            # Alphanumerical token
            can_be_acronym = False

            if not already_consumed:
                could_be_url = starts_as_url(string, i)
                could_be_email = email_lookahead(string, i)

                if could_be_url:
                    token_type = 'url'
                elif could_be_email:
                    token_type = 'email'

                while j < l:
                    if string[j].isspace():
                        break

                    if could_be_url or could_be_email:
                        if string[j] == ',':
                            break

                    elif string[j] == '-' or string[j] == '_':
                        if j + 1 >= l:
                            break

                        if string[j + 1].isspace():
                            break

                        j += 1
                        continue

                    elif not string[j].isalnum():

                        # Handling acronyms
                        if string[j] == '.' and string[j - 1].isupper():
                            j += 1
                            can_be_acronym = True
                            continue

                        break

                    j += 1

            before = string[i:j]

            if can_be_acronym:
                if all(len(t) <= 1 for t in before.split('.')):
                    yield ('word', before)

                else:
                    for t in POINT_SPLITTER_RE.split(before)[:-1]:
                        yield ('word' if t != '.' else 'punct', t)

                i = j
                continue

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
                        yield (token_type, before)
                        yield (token_type, string[j] + after)

                    elif (
                        (before.endswith('n') and after == 't') or
                        after in FRENCH_EXCEPTIONS or
                        '-' in before
                    ):
                        yield (token_type, string[i:k])

                    elif (
                        (
                            after[0] != 'h' and
                            is_consonant(before[-1]) and
                            is_consonant(after[0])
                        ) or
                        before in IRISH
                    ):
                        yield (token_type, before + string[j] + after)

                    else:
                        yield (token_type, before + string[j])
                        i = j + 1
                        continue

                else:
                    yield (token_type, before)

                j = k

            # Handling abbreviations
            elif j < l - 1 and string[j] == '.' and before.lower() in ABBREVIATIONS:
                yield (token_type, before + '.')
                j += 1

            # Handling regular word
            else:
                yield (token_type, before)

            i = j

    def __call__(self, string):
        return self.tokenize(string)
