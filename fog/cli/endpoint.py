#!/usr/bin/env python
# =============================================================================
# Fog CLI Endpoint
# =============================================================================
#
# CLI Interface of the Fog library.
#
from argparse import ArgumentParser

from fog.cli.cluster import cluster_action, CLUSTERING_ROUTINES


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='action to execute', title='actions', dest='action')

    cluster = subparsers.add_parser('cluster')
    cluster.add_argument('file', help='csv file to cluster')
    cluster.add_argument('column', help='target column')
    cluster.add_argument('-a', '--algorithm', help='algorithm to use', default='fingerprint_collision', choices=list(CLUSTERING_ROUTINES.keys()))

    args = parser.parse_args()

    if args.action == 'cluster':
        cluster_action(args)


if __name__ == '__main__':
    main()
