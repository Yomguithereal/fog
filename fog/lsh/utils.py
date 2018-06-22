# =============================================================================
# Fog LSH Utilities
# =============================================================================
#
# Miscellaneous helper functions used by the LSH module.
#
import binascii

UINT32_MASK = 0xFFFFFFFF
POPCOUNT_TABLE16 = [0] * (2 ** 16)

for i in range(len(POPCOUNT_TABLE16)):
    POPCOUNT_TABLE16[i] = (i & 1) + POPCOUNT_TABLE16[i >> 1]


def is_power_of_two(x):
    return (x & (x - 1))


def crc32(x):
    return binascii.crc32(x.encode()) & UINT32_MASK


def popcount(x):
    return bin(x).count('1')


def popcount16(x):
    return POPCOUNT_TABLE16[x & 0xFFFF]


def popcount32(x):
    return (
        POPCOUNT_TABLE16[x & 0xFFFF] + POPCOUNT_TABLE16[(x >> 16) & 0xFFFF]
    )


def popcount64(x):
    x -= (x >> 1) & 0x5555555555555555
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f
    return ((x * 0x0101010101010101) & 0xffffffffffffffff) >> 56
