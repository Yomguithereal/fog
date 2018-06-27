# =============================================================================
# Fog Cluster CLI Action UI
# =============================================================================
#
# Urwid UI for the cluster action.
#
import signal
from urwid import (
    Columns,
    ExitMainLoop,
    Filler,
    LineBox,
    ListBox,
    MainLoop,
    Padding,
    SimpleFocusListWalker,
    Text
)


def exit(*args):
        raise ExitMainLoop()


class ClusteringUI(object):
    def __init__(self, rows, clusters):

        # Composing the UI
        body = SimpleFocusListWalker([Text(str(cluster)) for cluster in clusters])
        clusters_list_box = ListBox(body)

        left_box = Padding(clusters_list_box, left=1, right=1)
        right_box = Padding(Text('Some other thing'), left=1, right=1)

        left_column = LineBox(left_box, title='Fog Clustering', title_align='left')
        right_colum = LineBox(Filler(right_box, 'top'), title='Stats', title_align='left')

        columns = Columns([('weight', 0.7, left_column), ('weight', 0.3, right_colum)])

        # Loop
        self.loop = MainLoop(columns, unhandled_input=self.unhandled_input)

        # Handling signals
        signal.signal(signal.SIGINT, exit)
        signal.signal(signal.SIGTERM, exit)

        # Properties
        self.rows = rows
        self.clusters = clusters
        self.current_cluster = 0

        # Activable components
        self.left_box = left_box

    def run(self):
        self.loop.run()

    def unhandled_input(self, key):
        if key in ('q', 'Q', 'esc'):
            raise ExitMainLoop()
