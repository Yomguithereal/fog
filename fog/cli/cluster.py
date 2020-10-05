# =============================================================================
# Fog Cluster CLI Action
# =============================================================================
#
# Logic of the cluster CLI action enabling the user to cluster the content of
# a CSV file.
#
from collections import Counter
from datetime import datetime
from timeit import default_timer as timer

from fog.cli.utils import custom_reader
from fog.cli.reporting import RENDERERS
from fog.clustering import (
    key_collision
)
from fog.key import fingerprint

CLUSTERING_ROUTINES = {
    'fingerprint_collision': {
        'name': 'Fingerpint collision',
        'fn': key_collision,
        'kwargs': {
            'key': fingerprint
        }
    }
}


def cluster_action(namespace):
    routine = CLUSTERING_ROUTINES[namespace.algorithm]

    lines = 0

    headers, position, reader = custom_reader(namespace.file, namespace.column)

    values = Counter()

    for line in reader:
        lines += 1
        values[line[position]] += 1

    start = timer()
    clusters = routine['fn'](values.keys(), **routine['kwargs'])
    end = timer() - start

    meta = {
        'algorithm': namespace.algorithm,
        'took': end,
        'date': datetime.now(),
        'lines': lines
    }

    renderer = RENDERERS[namespace.type]

    renderer(namespace.output, meta, values, list(clusters))
