def ngrams_count(l, n):
    return l - (n - 1)

def ngrams_upper_bound(l, m):
    n = l // m

    return ngrams_count(l, n) + ngrams_count(l, n + 1)

def powerset(a, b):
    return (a + 1) * (b + 1) - 1

def keys_count(a, b):
    return powerset(a, b) * 2 - a - b

def formula(k):
    if k % 2 != 0:
        return ((k + 1) ** 2) / 2 + k + 1
    else:
        return (k ** 2) / 2 + 2 * k + 1

def multiset_powerset(multiset):
    n = len(multiset)
    c = [0] * n

    while True:
        changed = False

        i = n - 1
        while i >= 0 and not changed:
            if c[i] < multiset[i]:

                # Increment
                c[i] += 1
                changed = True
            else:

                # Roll over
                c[i] = 0

            i -= 1

        if changed:
            yield c
        else:
            break

def keys(k, string):
    m = k + 1
    l = len(string)

    a = l % m
    b = m - a

    nb = l // m
    na = nb + 1

    for ca, cb in multiset_powerset((a, b)):
        s = ca * na + cb * nb
        o = (ca + cb) - 1
        if ca > 0:
            yield (o, string[s - na:s])
        if cb > 0:
            yield (o, string[s - nb:s])

if __name__ == '__main__':
    for k in range(1, 10):

        m = k + 1
        l_max = m * 2 - 1
        l_med = m + m // 2

        a = l_med % m
        b = m - a

        print('Stats for k = %i:' % k)
        print('  - k (distance threshold): %i' % k)
        print('  - m (number of chunks): %i' % m)
        print('  - min nb of keys: %i (%i with tr)' % (m, m * 2))
        print('  - max nb of keys: %i (with formula: %i)' % (keys_count(a, b), formula(k)))
        print('  - %s%s (%i, %i)' % ('a' * a, 'b' * b, a, b))
        print()
