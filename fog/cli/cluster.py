# =============================================================================
# Fog Cluster CLI Action
# =============================================================================
#
# Logic of the cluster CLI action enabling the user to cluster the content of
# a CSV file.
#
import csv
import re
from collections import Counter
from datetime import datetime
from timeit import default_timer as timer

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


def escape_string(string):
    return string.replace('"', '\\"').replace('\n', '\\n')


def print_toml_report(meta, values, clusters):
    print('[info]')
    print('date = %s' % meta['date'].isoformat().split('.')[0])
    print('algorithm = "%s"' % meta['algorithm'])
    print()
    print('[stats]')
    print('lines = %i' % meta['lines'])
    print('nb_distinct_values = %i' % len(values))
    print('nb_clusters = %i' % len(clusters))
    print('took = %2f' % meta['took'])
    print()

    for i, cluster in enumerate(clusters):
        print('[[cluster]]')
        print('id = %i' % i)
        print('nb_values = %i' % len(cluster))

        # Sorting by affected rows
        sorted_values = sorted(cluster, key=lambda v: values[v], reverse=True)
        max_length = len(max(cluster, key=len))

        print('harmonized = "%s"' % escape_string(sorted_values[0]))
        print('values =  [')
        for value in sorted_values:
            print('  [["%s"],%s [%i]],' % (
                escape_string(value),
                ' ' * (max_length - len(value)),
                values[value]
            ))

        print(']')

        print('harmonize = false')

        print()


def cluster_action(namespace):
    routine = CLUSTERING_ROUTINES[namespace.algorithm]

    lines = 0
    with open(namespace.file, 'r') as f:
        reader = csv.DictReader(f)

        values = Counter()

        for line in reader:
            lines += 1
            values[line[namespace.column]] += 1

    start = timer()
    clusters = routine['fn'](values.keys(), **routine['kwargs'])
    end = timer() - start

    meta = {
        'algorithm': namespace.algorithm,
        'took': end,
        'date': datetime.now(),
        'lines': lines
    }

    print_toml_report(meta, values, list(clusters))
