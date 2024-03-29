# =============================================================================
# Fog Clustering Unit Tests Utilities
# =============================================================================


class Clusters(object):
    def __init__(self, clusters):
        self.groups = set(tuple(sorted(values, key=str)) for values in clusters)

    def __eq__(self, other):
        return self.groups == other.groups

    def __iter__(self):
        return iter(self.groups)

    def __len__(self):
        return len(self.groups)

    def __repr__(self):
        return 'Clusters(%s)' % self.groups.__repr__()
