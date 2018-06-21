# =============================================================================
# Fog LSH Utilities
# =============================================================================
#
# Miscellaneous helper functions used by the LSH module.
#
import binascii

UINT32_MASK = 0xFFFFFFFF


def crc32(x):
    return binascii.crc32(x.encode()) & UINT32_MASK


def popcount(x):
    x -= (x >> 1) & 0x5555555555555555
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f
    return ((x * 0x0101010101010101) & 0xffffffffffffffff) >> 56
