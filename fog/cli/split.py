# =============================================================================
# Fog Split CLI Action
# =============================================================================
#
# Logic of the split CLI action that can split multi-valued column cells
# into different lines.
#
import csv

from fog.cli.utils import custom_reader


def split_action(namespace):
    headers, position, reader = custom_reader(namespace.file, namespace.column)

    if namespace.target_column is not None:
        headers.append(namespace.target_column)

    if namespace.rename_column is not None:
        headers[position] = namespace.rename_column

    writer = csv.writer(namespace.output)
    writer.writerow(headers)

    for line in reader:
        values = line[position]

        if len(values) == 0:
            writer.writerow(line)
            continue

        for value in values.split(namespace.separator):

            if namespace.target_column:
                line.append(value)
            else:
                line[position] = value

            writer.writerow(line)
