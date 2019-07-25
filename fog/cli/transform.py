# =============================================================================
# Fog Transform CLI Action
# =============================================================================
#
# Logic of the transform CLI action enabling the user to edit cell in batch.
#
import csv
from unidecode import unidecode
from fog.cli.utils import custom_reader
from fog.key import fingerprint
from fog.utils import squeeze

OPERATIONS = {
    'fingerprint': fingerprint,
    'len': len,
    'lower': lambda x: x.lower(),
    'squeeze': squeeze,
    'strip': lambda x: x.strip(),
    'unidecode': unidecode,
    'upper': lambda x: x.upper()
}


def transform_action(namespace):

    # TODO: validate operation_chain
    operation_chain = None

    if not namespace.eval:
        operation_chain = [OPERATIONS[o] for o in namespace.operations.split(',')]

    headers, position, reader = custom_reader(namespace.file, namespace.column)

    if namespace.target_column is not None:
        if namespace.after:
            headers = headers[:position + 1] + [namespace.target_column] + headers[position + 1:]
        else:
            headers.append(namespace.target_column)

    writer = csv.writer(namespace.output)
    writer.writerow(headers)

    for line in reader:
        new_value = line[position]

        if namespace.eval:
            new_value = eval(namespace.operations, None, {
                'unidecode': unidecode,
                'value': new_value
            })
        else:
            for op in operation_chain:
                new_value = op(new_value)

        if namespace.target_column is not None:
            if namespace.after:
                line = line[:position + 1] + [new_value] + line[position + 1:]
            else:
                line.append(new_value)
        else:
            line[position] = new_value

        writer.writerow(line)
