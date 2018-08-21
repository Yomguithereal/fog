# =============================================================================
# Fog CLI Helpers
# =============================================================================
#
# Miscellaneous helpers used by the CLI tools.
#
import csv


def custom_reader(f, target_header):
    reader = csv.reader(f)

    headers = next(reader, None)

    position = headers.index(target_header)

    return headers, position, reader
