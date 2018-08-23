# =============================================================================
# Fog CLI Utils
# =============================================================================
#
# Miscellaneous helpers used by the CLI tools.
#
import csv


def custom_reader(f, target_header):
    # sniffer = csv.Sniffer()
    # dialect = sniffer.sniff(f.read(1024))
    # f.seek(0)

    reader = csv.reader(f)

    headers = next(reader, None)

    position = headers.index(target_header)

    return headers, position, reader
