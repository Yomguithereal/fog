# =============================================================================
# Fog Word Tokenizer
# =============================================================================
#
# A general purpose word tokenizer able to consider a lot of edge case and
# typical entities all while remaining mostly language agnostic wrt languages
# separating their words using whitespace (not the asian languages, for instance).
#
# It was mostly designed for French and English, but it probably works with
# other latin languages out of the box.
#
# The resulting token streams are tagged by entity types (not part-of-speech).
#
# Some design choices:
#  * We chose to only tag as numbers strings that could be parsed as ints or floats
#    without ambiguity. This means word tokens may contain things that
#    could be considered as numbers, but you can analyze them further down the line.
#
# Here is a list of things we don't handle (yet):
#   * Complex graphemes such as: u̲n̲d̲e̲r̲l̲i̲n̲e̲d̲ or ārrive
#   * Multi-line hyphenation schemes
#   * Junk found in the middle of a word token
#
import re
from html import unescape
from emoji import get_emoji_regexp
from unidecode import unidecode
from ebbe import with_next
from typing import Optional, Iterable

DECIMALS = ['.', ',']
IDENTIFIER_PARTS = ['-', '_']
APOSTROPHES = ['\'', '’']
IRISH = ['O', 'o']
VOWELS_PATTERN = 'aáàâäąåoôóøeéèëêęiíïîıuúùûüyÿæœAÁÀÂÄĄÅOÓÔØEÉÈËÊĘIİÍÏÎYŸUÚÙÛÜÆŒ'
CONSONANTS_RE = re.compile(r'^[^%s]$' % VOWELS_PATTERN)
EMAIL_LOOKAHEAD_RE = re.compile(r'^[A-Za-z0-9!#$%&*+\-/=?^_`{|}~]{1,64}@')
SMILEY_RE = re.compile(r'^(?:[\-]+>|<[\-]+|[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP/\:\}\{@\|\\]|[\)\]\(\[dDpP/\:\}\{@\|\\][\-o\*\']?[:;=8]|[<:]3)')
EMOJI_RE = get_emoji_regexp()
POINT_SPLITTER_RE = re.compile(r'(\.)')
LENGTHENING_RE = re.compile(r'(.)\1{2,}')

ENGLISH_CONTRACTIONS = ['ll', 're', 'm', 's', 've', 'd']
FRENCH_EXCEPTIONS = ['hui']
FRENCH_UNION_TARGETS = {
    'je',
    'tu',
    'il',
    'ils',
    'elle',
    'elles',
    'nous',
    'vous',
    'ils',
    'on',
    'le',
    'la',
    'les',
    'moi',
    'toi',
    'lui',
    'y'
}
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

TOKEN_TYPES = {
    'word',
    'number',
    'punct',
    'emoji',
    'smiley',
    'url',
    'email',
    'hashtag',
    'mention'
}


def is_ascii_junk(c):
    return c <= '\x1f'


def is_valid_twitter_char(c):
    return (
        c == '_' or
        (c >= '0' and c <= '9') or
        (c >= 'a' and c <= 'z') or
        (c >= 'A' and c <= 'Z')
    )


def is_consonant(c):
    return bool(CONSONANTS_RE.match(c))


def starts_as_url(string):
    return string.startswith('http://') or string.startswith('https://')


def email_lookahead(string):
    return bool(EMAIL_LOOKAHEAD_RE.match(string))


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
        if (
            next_item is not None and
            item[0] == 'emoji' and
            next_item[0] == 'punct' and
            next_item[1] == '\ufe0f'
        ):
            skip_next = True
            yield ('emoji', item[1] + next_item[1])

        else:
            yield item


def reduce_lenghtening(string):
    return LENGTHENING_RE.sub(r'\1\1\1', string)


def validate_token_types(types):
    for token_type in types:
        if token_type not in TOKEN_TYPES:
            raise TypeError('unknown token type: %s' % token_type)


class WordTokenizer(object):
    def __init__(
        self,
        lower: bool = False,
        unidecode: bool = False,
        reduce_words: bool = False,
        decode_html_entities: bool = False,
        min_word_length: Optional[int] = None,
        max_word_length: Optional[int] = None,
        stoplist: Optional[Iterable[str]] = None,
        keep: Optional[Iterable[str]] = None,
        drop: Optional[Iterable[str]] = None
    ):
        self.lower = lower
        self.unidecode = unidecode
        self.reduce_words = reduce_words
        self.decode_html_entities = decode_html_entities
        self.min_word_length = min_word_length
        self.max_word_length = max_word_length
        self.stoplist = stoplist
        self.keep = keep
        self.drop = drop

        if self.keep is not None and self.drop is not None:
            raise TypeError('giving both `keep` and `drop` makes no sense')

        if self.min_word_length is not None and self.max_word_length is not None:
            if self.min_word_length >= self.max_word_length:
                raise TypeError('`min_word_length` should be less than `max_word_length`')

        if self.stoplist is not None:
            if not isinstance(self.stoplist, set):
                self.stoplist = set(self.stoplist)

            if self.lower:
                self.stoplist = set(token.lower() for token in self.stoplist)

        if self.keep:
            self.keep = set(self.keep)
            validate_token_types(self.keep)

        if self.drop:
            self.drop = set(self.drop)
            validate_token_types(self.drop)

        self.__only_defaults = True

        if (
            self.lower or
            self.unidecode or
            self.reduce_words or
            self.min_word_length is not None or
            self.max_word_length is not None or
            self.stoplist is not None or
            self.keep is not None or
            self.drop is not None
        ):
            self.__only_defaults = False

    def __tokenize(self, string):
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

            lookahead = string[i:i + 64]  # NOTE: 64 because of emails

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
                j = i + 1

                while j < l:
                    n = string[j]

                    if (
                        n.isspace() or
                        n.isalnum() or
                        is_ascii_junk(n) or
                        n == '#' or
                        n == '@'
                    ):
                        break

                    j += 1

                yield from punct_emoji_iter(string[i:j])
                i = j

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
                    n = string[j]

                    if n.isspace():
                        break

                    if not n.isdigit():
                        if last_char in DECIMALS:
                            j -= 1
                            break

                        if (
                            last_char != '-' and
                            (
                                n.isalpha() or
                                n in IDENTIFIER_PARTS
                            )
                        ):
                            already_consumed = False
                            token_type = 'word'
                            break

                        elif n not in DECIMALS:
                            break

                        elif chosen_decimal is not None:
                            break

                        else:
                            chosen_decimal = n

                    last_char = n
                    token_type = 'number'
                    j += 1

                if already_consumed and j > i + 1 and string[j - 1] in DECIMALS:
                    j -= 1

            # Alphanumerical token
            can_be_acronym = False

            if not already_consumed:
                could_be_url = starts_as_url(lookahead)
                could_be_email = email_lookahead(lookahead)

                if could_be_url:
                    token_type = 'url'
                elif could_be_email:
                    token_type = 'email'

                while j < l:
                    n = string[j]

                    if n.isspace():
                        break

                    if could_be_url or could_be_email:
                        if n == ',':
                            break

                    elif n in IDENTIFIER_PARTS:
                        if j + 1 >= l:
                            break

                        if string[j + 1].isspace():
                            break

                        j += 1
                        continue

                    elif not n.isalnum():

                        # Handling acronyms
                        if n == '.' and string[j - 1].isupper():
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

                # Handling unions that should be split
                hyphens = before.count('-')

                if hyphens == 2 and '-t-' in before:
                    for t in before.split('-'):
                        yield (token_type, t)

                elif hyphens == 1:
                    a, b = before.split('-')

                    if b in FRENCH_UNION_TARGETS:
                        yield (token_type, a)
                        yield (token_type, b)

                    else:
                        yield (token_type, before)

                else:
                    yield (token_type, before)

            i = j

    def tokenize(self, string):
        if self.decode_html_entities:
            string = unescape(string)

        if self.__only_defaults:
            yield from self.__tokenize(string)
            return

        for token in self.__tokenize(string):
            token_type, token_value = token

            if self.keep is not None and token_type not in self.keep:
                continue

            elif self.drop is not None and token_type in self.drop:
                continue

            elif token_type == 'word':
                if self.lower:
                    token_value = token_value.lower()

                if self.unidecode:
                    token_value = unidecode(token_value)

                if self.reduce_words:
                    token_value = reduce_lenghtening(token_value)

                if self.min_word_length is not None and len(token_value) < self.min_word_length:
                    continue

                elif self.max_word_length is not None and len(token_value) > self.max_word_length:
                    continue

                token = (token_type, token_value)

            if self.stoplist is not None and token_value in self.stoplist:
                continue

            yield token

    def __call__(self, string):
        return self.tokenize(string)
