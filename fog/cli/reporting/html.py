# =============================================================================
# Fog Cluster HTML Reporting Utilities
# =============================================================================
#
# Function used to render a clustering result into a HTML file.
#
import datetime


def print_html_report(file, meta, values, clusters):

    def p(*args):
        print(*args, file=file)

    p('<html>')
    p('  <head>')
    p('    <title>Clustering result</title>')
    p('    <style>')
    p('      td {padding-right: 10px};')
    p('    </style>')
    p('  </head>')
    p('  <body>')
    p('    <h1>Clustering result</h1>')
    p('    <div>')
    p('      <h2>Information:</h2>')
    p('      <table>')
    p('        <tr>')
    p('          <td>')
    p('            <b>Date</b>')
    p('          </td>')
    p('          <td>')
    p('            %s' % meta['date'].isoformat().split('T')[0])
    p('          </td>')
    p('        </tr>')
    p('        <tr>')
    p('          <td>')
    p('            <b>Algorithm used</b>')
    p('          </td>')
    p('          <td>')
    p('            %s' % meta['algorithm'])
    p('          </td>')
    p('        </tr>')
    p('      </table>')
    p('    </div>')
    p('    <div>')
    p('      <h2>Statistics:</h2>')
    p('      <table>')
    p('        <tr>')
    p('          <td>')
    p('            <b>Lines</b>')
    p('          </td>')
    p('          <td>')
    p('            {:,}'.format(meta['lines']))
    p('          </td>')
    p('        </tr>')
    p('        <tr>')
    p('          <td>')
    p('            <b>Distinct values</b>')
    p('          </td>')
    p('          <td>')
    p('            {:,}'.format(len(values)))
    p('          </td>')
    p('        </tr>')
    p('        <tr>')
    p('          <td>')
    p('            <b>Found clusters</b>')
    p('          </td>')
    p('          <td>')
    p('            {:,}'.format(len(clusters)))
    p('          </td>')
    p('        </tr>')
    p('        <tr>')
    p('          <td>')
    p('            <b>Took</b>')
    p('          </td>')
    p('          <td>')
    p('            %s' % datetime.timedelta(microseconds=meta['took']))
    p('          </td>')
    p('        </tr>')
    p('      </table>')
    p('    </div>')
    p('    <div>')
    p('      <h2>Clusters:</h2>')

    for i, cluster in enumerate(clusters):
        p('      <p>')
        p('        Cluster n°%i (%i unique values, %i affected rows):' % (i + 1, len(cluster), sum(values[v] for v in cluster)))
        p('      <ul>')

        # Sorting by affected rows
        sorted_values = sorted(cluster, key=lambda v: values[v], reverse=True)

        for v in sorted_values:
            p('        <li>')
            p('          %s' % v)
            p('        </li>')

        p('      </ul>')
        p('      </p>')

    p('    </div>')
    p('  </body>')
    p('<html>')
