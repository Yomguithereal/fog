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
from fog.cli.split import split_action
from fog.cli.transform import transform_action, OPERATIONS

SUBPARSERS = {}


def main():
    parser = ArgumentParser(prog='fog')
    subparsers = parser.add_subparsers(help='action to execute', title='actions', dest='action')

    cluster_subparser = subparsers.add_parser('cluster', description='Fuzzy clustering on a CSV column.')
    cluster_subparser.add_argument('column', help='column')
    cluster_subparser.add_argument('file', help='csv file to cluster', type=FileType('r'), default=sys.stdin, nargs='?')
    cluster_subparser.add_argument('-o', '--output', help='output file', type=FileType('w'), default=sys.stdout)
    cluster_subparser.add_argument('-a', '--algorithm', help='algorithm to use', default='fingerprint_collision', choices=list(CLUSTERING_ROUTINES.keys()))
    cluster_subparser.add_argument('-t', '--type', help='reporting file type', default='toml', choices=['html', 'toml'])
    SUBPARSERS['cluster'] = cluster_subparser

    split_subparser = subparsers.add_parser('split', description='Split a multivalued column into different lines.')
    split_subparser.add_argument('column', help='column')
    split_subparser.add_argument('file', help='csv file to split', type=FileType('r'), default=sys.stdin, nargs='?')
    split_subparser.add_argument('-o', '--output', help='output file', type=FileType('w'), default=sys.stdout)
    split_subparser.add_argument('-s', '--separator', help='values separator. Defaults to "|".', default='|')
    split_subparser.add_argument('-t', '--target-column', help='name of the column to create')
    split_subparser.add_argument('-r', '--rename-column', help='new name for the column')
    SUBPARSERS['split'] = split_subparser

    transform_subparser = subparsers.add_parser('transform', description='Transform the values of a column in batch.')
    transform_subparser.add_argument('column', help='column')
    transform_subparser.add_argument('operations', help='operations to apply, separated by commas {%s}' % ','.join(list(OPERATIONS.keys())))
    transform_subparser.add_argument('file', help='csv file to transform', type=FileType('r'), default=sys.stdin, nargs='?')
    transform_subparser.add_argument('-o', '--output', help='output file', type=FileType('w'), default=sys.stdout)
    transform_subparser.add_argument('-t', '--target-column', help='name of the column to create')
    transform_subparser.add_argument('-a', '--after', help='whether to add the new column just after the original one', action='store_true')
    transform_subparser.add_argument('--eval', help='evaluate the operations as a python expression rather than using an operation chain', action='store_true')
    SUBPARSERS['transform'] = transform_subparser

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

    if args.action == 'split':
        split_action(args)

    if args.action == 'transform':
        transform_action(args)

    if args.action is None:
        parser.print_help()


if __name__ == '__main__':
    main()
