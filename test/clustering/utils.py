# =============================================================================
# Fog Clustering Unit Tests Utilities
# =============================================================================


class Clusters(object):
    def __init__(self, clusters):
        self.groups = set(tuple(sorted(values)) for values in clusters)

    def __eq__(self, other):
        return self.groups == other.groups
