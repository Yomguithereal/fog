#!/usr/bin/env python
# =============================================================================
# Fog CLI Endpoint
# =============================================================================
#
# CLI Interface of the Fog library.
#
from argparse import ArgumentParser

from fog.cli.cluster import cluster_action, CLUSTERING_ROUTINES

SUBPARSERS = {}


def main():
    parser = ArgumentParser(prog='fog')
    subparsers = parser.add_subparsers(help='action to execute', title='actions', dest='action')

    help_suparser = subparsers.add_parser('help')
    help_suparser.add_argument('subcommand', help='name of the subcommand')
    SUBPARSERS['help'] = help_suparser

    cluster_subparser = subparsers.add_parser('cluster', description='Fuzzy clustering on a CSV column.')
    cluster_subparser.add_argument('file', help='csv file to cluster')
    cluster_subparser.add_argument('column', help='target column')
    cluster_subparser.add_argument('-a', '--algorithm', help='algorithm to use', default='fingerprint_collision', choices=list(CLUSTERING_ROUTINES.keys()))
    SUBPARSERS['cluster'] = cluster_subparser

    args = parser.parse_args()

    if args.action == 'help':
        target_subparser = SUBPARSERS.get(args.subcommand)

        if target_subparser is None:
            parser.print_help()
        else:
            target_subparser.print_help()

    if args.action == 'cluster':
        cluster_action(args)

    if args.action is None:
        parser.print_help()


if __name__ == '__main__':
    main()
