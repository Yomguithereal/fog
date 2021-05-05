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
EMAIL_LOOKAHEAD_RE = re.compile(r'^[A-Za-z0-9!#$%&*+\-/=?^_`{|}~]{1,64}@')
SMILEY_RE = re.compile(r'^(?:[\-]+>|<[\-]+|[<>]?[:;=8][\-o\*\']?[\)\]\(\[dDpP/\:\}\{@\|\\]|[\)\]\(\[dDpP/\:\}\{@\|\\][\-o\*\']?[:;=8]|[<:]3)')
PUNCT_CODES = [33, 34, 35, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 58, 59, 63, 64, 91, 92, 93, 95, 123, 125, 161, 167, 171, 182, 183, 187, 191, 894, 903, 1370, 1371, 1372, 1373, 1374, 1375, 1417, 1418, 1470, 1472, 1475, 1478, 1523, 1524, 1545, 1546, 1548, 1549, 1563, 1566, 1567, 1642, 1643, 1644, 1645, 1748, 1792, 1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1805, 2039, 2040, 2041, 2096, 2097, 2098, 2099, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2142, 2404, 2405, 2416, 2800, 3572, 3663, 3674, 3675, 3844, 3845, 3846, 3847, 3848, 3849, 3850, 3851, 3852, 3853, 3854, 3855, 3856, 3857, 3858, 3860, 3898, 3899, 3900, 3901, 3973, 4048, 4049, 4050, 4051, 4052, 4057, 4058, 4170, 4171, 4172, 4173, 4174, 4175, 4347, 4960, 4961, 4962, 4963, 4964, 4965, 4966, 4967, 4968, 5120, 5741, 5742, 5787, 5788, 5867, 5868, 5869, 5941, 5942, 6100, 6101, 6102, 6104, 6105, 6106, 6144, 6145, 6146, 6147, 6148, 6149, 6150, 6151, 6152, 6153, 6154, 6468, 6469, 6686, 6687, 6816, 6817, 6818, 6819, 6820, 6821, 6822, 6824, 6825, 6826, 6827, 6828, 6829, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 7164, 7165, 7166, 7167, 7227, 7228, 7229, 7230, 7231, 7294, 7295, 7360, 7361, 7362, 7363, 7364, 7365, 7366, 7367, 7379, 8208, 8209, 8210, 8211, 8212, 8213, 8214, 8215, 8216, 8217, 8218, 8219, 8220, 8221, 8222, 8223, 8224, 8225, 8226, 8227, 8228, 8229, 8230, 8231, 8240, 8241, 8242, 8243, 8244, 8245, 8246, 8247, 8248, 8249, 8250, 8251, 8252, 8253, 8254, 8255, 8256, 8257, 8258, 8259, 8261, 8262, 8263, 8264, 8265, 8266, 8267, 8268, 8269, 8270, 8271, 8272, 8273, 8275, 8276, 8277, 8278, 8279, 8280, 8281, 8282, 8283, 8284, 8285, 8286, 8317, 8318, 8333, 8334, 8968, 8969, 8970, 8971, 9001, 9002, 10088, 10089, 10090, 10091, 10092, 10093, 10094, 10095, 10096, 10097, 10098, 10099, 10100, 10101, 10181, 10182, 10214, 10215, 10216, 10217, 10218, 10219, 10220, 10221, 10222, 10223, 10627, 10628, 10629, 10630, 10631, 10632, 10633, 10634, 10635, 10636, 10637, 10638, 10639, 10640, 10641, 10642, 10643, 10644, 10645, 10646, 10647, 10648, 10712, 10713, 10714, 10715, 10748, 10749, 11513, 11514, 11515, 11516, 11518, 11519, 11632, 11776, 11777, 11778, 11779, 11780, 11781, 11782, 11783, 11784, 11785, 11786, 11787, 11788, 11789, 11790, 11791, 11792, 11793, 11794, 11795, 11796, 11797, 11798, 11799, 11800, 11801, 11802, 11803, 11804, 11805, 11806, 11807, 11808, 11809, 11810, 11811, 11812, 11813, 11814, 11815, 11816, 11817, 11818, 11819, 11820, 11821, 11822, 11824, 11825, 11826, 11827, 11828, 11829, 11830, 11831, 11832, 11833, 11834, 11835, 11836, 11837, 11838, 11839, 11840, 11841, 11842, 11843, 11844, 12289, 12290, 12291, 12296, 12297, 12298, 12299, 12300, 12301, 12302, 12303, 12304, 12305, 12308, 12309, 12310, 12311, 12312, 12313, 12314, 12315, 12316, 12317, 12318, 12319, 12336, 12349, 12448, 12539, 42238, 42239, 42509, 42510, 42511, 42611, 42622, 42738, 42739, 42740, 42741, 42742, 42743, 43124, 43125, 43126, 43127, 43214, 43215, 43256, 43257, 43258, 43260, 43310, 43311, 43359, 43457, 43458, 43459, 43460, 43461, 43462, 43463, 43464, 43465, 43466, 43467, 43468, 43469, 43486, 43487, 43612, 43613, 43614, 43615, 43742, 43743, 43760, 43761, 44011, 64830, 64831, 65040, 65041, 65042, 65043, 65044, 65045, 65046, 65047, 65048, 65049, 65072, 65073, 65074, 65075, 65076, 65077, 65078, 65079, 65080, 65081, 65082, 65083, 65084, 65085, 65086, 65087, 65088, 65089, 65090, 65091, 65092, 65093, 65094, 65095, 65096, 65097, 65098, 65099, 65100, 65101, 65102, 65103, 65104, 65105, 65106, 65108, 65109, 65110, 65111, 65112, 65113, 65114, 65115, 65116, 65117, 65118, 65119, 65120, 65121, 65123, 65128, 65130, 65131, 65281, 65282, 65283, 65285, 65286, 65287, 65288, 65289, 65290, 65292, 65293, 65294, 65295, 65306, 65307, 65311, 65312, 65339, 65340, 65341, 65343, 65371, 65373, 65375, 65376, 65377, 65378, 65379, 65380, 65381, 65792, 65793, 65794, 66463, 66512, 66927, 67671, 67871, 67903, 68176, 68177, 68178, 68179, 68180, 68181, 68182, 68183, 68184, 68223, 68336, 68337, 68338, 68339, 68340, 68341, 68342, 68409, 68410, 68411, 68412, 68413, 68414, 68415, 68505, 68506, 68507, 68508, 69703, 69704, 69705, 69706, 69707, 69708, 69709, 69819, 69820, 69822, 69823, 69824, 69825, 69952, 69953, 69954, 69955, 70004, 70005, 70085, 70086, 70087, 70088, 70089, 70093, 70107, 70109, 70110, 70111, 70200, 70201, 70202, 70203, 70204, 70205, 70313, 70731, 70732, 70733, 70734, 70735, 70747, 70749, 70854, 71105, 71106, 71107, 71108, 71109, 71110, 71111, 71112, 71113, 71114, 71115, 71116, 71117, 71118, 71119, 71120, 71121, 71122, 71123, 71124, 71125, 71126, 71127, 71233, 71234, 71235, 71264, 71265, 71266, 71267, 71268, 71269, 71270, 71271, 71272, 71273, 71274, 71275, 71276, 71484, 71485, 71486, 72769, 72770, 72771, 72772, 72773, 72816, 72817, 74864, 74865, 74866, 74867, 74868, 92782, 92783, 92917, 92983, 92984, 92985, 92986, 92987, 92996, 113823, 121479, 121480, 121481, 121482, 121483, 125278, 125279]
PUNCT = set(chr(i) for i in PUNCT_CODES)

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


def email_lookahead(string, i):
    return bool(EMAIL_LOOKAHEAD_RE.match(string[i:i + 64]))


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

            # Breaking punctuation apart
            elif not c.isalnum() and c not in APOSTROPHES and c != '-':

                # Surrogates
                while i + 1 < l and string[i + 1] == '\u200d':
                    c += string[i + 1:i + 3]
                    i += 2

                yield ('punct' if c in PUNCT else 'emoji', c)
                i += 1
                continue

            # Consuming token
            j = i + 1

            if can_be_hashtag and not is_ascii_alpha(string[j]):
                yield ('punct', c)
                i += 1
                continue

            token_type = 'word'

            # Mention and hashtag token
            if can_be_mention or can_be_hashtag:
                if can_be_mention:
                    token_type = 'mention'
                else:
                    token_type = 'hashtag'

                while j < l and is_valid_twitter_char(string[j]):
                    j += 1

            # Numerical token
            elif c.isdigit() or c == '-':
                token_type = 'number'

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

                    elif not string[j].isalnum():

                        # Handling acronyms
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
                        yield (token_type, before)
                        yield (token_type, string[j] + after)

                    elif (
                        (before.endswith('n') and after == 't') or
                        after in FRENCH_EXCEPTIONS
                    ):
                        yield (token_type, string[i:k])

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
