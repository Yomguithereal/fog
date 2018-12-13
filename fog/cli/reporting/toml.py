# =============================================================================
# Fog Cluster TOML Reporting Utilities
# =============================================================================
#
# Function used to render a clustering result into a TOML file.
#


def escape_string(string):
    return string.replace('"', '\\"').replace('\n', '\\n')


def print_toml_report(file, meta, values, clusters):

    def p(*args):
        print(*args, file=file)

    p('[info]')
    p('date = %s' % meta['date'].isoformat().split('.')[0])
    p('algorithm = "%s"' % meta['algorithm'])
    p()
    p('[stats]')
    p('lines = %i' % meta['lines'])
    p('nb_distinct_values = %i' % len(values))
    p('nb_clusters = %i' % len(clusters))
    p('took = %2f' % meta['took'])
    p()

    for i, cluster in enumerate(clusters):
        p('[[cluster]]')
        p('id = %i' % i)
        p('nb_values = %i' % len(cluster))
        p('nb_rows = %i' % sum(values[v] for v in cluster))

        # Sorting by affected rows
        sorted_values = sorted(cluster, key=lambda v: values[v], reverse=True)
        max_length = len(max(cluster, key=len))

        p('harmonized = "%s"' % escape_string(sorted_values[0]))
        p('values =  [')
        for value in sorted_values:
            p('  [["%s"],%s [%i]],' % (
                escape_string(value),
                ' ' * (max_length - len(value)),
                values[value]
            ))

        p(']')

        p('harmonize = false')
        p('')
