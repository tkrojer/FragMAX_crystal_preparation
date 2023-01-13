from ipywidgets import Layout

class layout(object):
    def __init__(self):
        self.vbox_layout = Layout(
                    display='flex',
                    flex_flow='column',
                    align_items='stretch',
#                    border='solid',
                    width='100%')
