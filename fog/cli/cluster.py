# =============================================================================
# Fog Cluster CLI Action
# =============================================================================
#
# Logic of the cluster CLI action enabling the user to cluster the content of
# a CSV file.
#
import csv
from collections import defaultdict

from fog.clustering import (
    key_collision
)

from fog.key import fingerprint


def fingerprint_collision(data):
    for cluster in key_collision(data, key=fingerprint):
        print(cluster)


CLUSTERING_ROUTINES = {
    'fingerprint_collision': fingerprint_collision
}


def cluster_action(namespace):
    routine = CLUSTERING_ROUTINES[namespace.algorithm]

    with open(namespace.file, 'r') as f:
        reader = csv.DictReader(f)

        rows = defaultdict(list)

        for line in reader:
            rows[line[namespace.column]].append(line)

    routine(rows.keys())
