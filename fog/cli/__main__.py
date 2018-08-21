#!/usr/bin/env python
# =============================================================================
# Fog CLI Endpoint
# =============================================================================
#
# CLI Interface of the Fog library.
#
import sys
from argparse import ArgumentParser, FileType

from fog.cli.cluster import cluster_action, CLUSTERING_ROUTINES
from fog.cli.multiplex import multiplex_action

SUBPARSERS = {}


def main():
    parser = ArgumentParser(prog='fog')
    subparsers = parser.add_subparsers(help='action to execute', title='actions', dest='action')

    cluster_subparser = subparsers.add_parser('cluster', description='Fuzzy clustering on a CSV column.')
    cluster_subparser.add_argument('column', help='target column')
    cluster_subparser.add_argument('file', help='csv file to cluster', type=FileType('r'), default=sys.stdin, nargs='?')
    cluster_subparser.add_argument('-a', '--algorithm', help='algorithm to use', default='fingerprint_collision', choices=list(CLUSTERING_ROUTINES.keys()))
    SUBPARSERS['cluster'] = cluster_subparser

    multiplex_subparser = subparsers.add_parser('multiplex', description='Multiplex a multivalued column into different lines.')
    multiplex_subparser.add_argument('column', help='target column')
    multiplex_subparser.add_argument('file', help='csv file to multiplex', type=FileType('r'), default=sys.stdin, nargs='?')
    multiplex_subparser.add_argument('-s', '--separator', help='values separator. Defaults to "|".', default='|')
    SUBPARSERS['multiplex'] = multiplex_subparser

    help_suparser = subparsers.add_parser('help')
    help_suparser.add_argument('subcommand', help='name of the subcommand')
    SUBPARSERS['help'] = help_suparser

    args = parser.parse_args()

    if args.action == 'help':
        target_subparser = SUBPARSERS.get(args.subcommand)

        if target_subparser is None:
            parser.print_help()
        else:
            target_subparser.print_help()

    if args.action == 'cluster':
        cluster_action(args)

    if args.action == 'multiplex':
        multiplex_action(args)

    if args.action is None:
        parser.print_help()


if __name__ == '__main__':
    main()
