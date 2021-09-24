import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label

class eln_entry(object):
    def __init__(self):
        self.grid_widget = widgets.GridspecLayout(10, 4)
        self.grid_widget[0,0] = Label("Title", layout=Layout(display="flex", justify_content="center"))

        self.title = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))

        # data created
        # date modified

        self.comment = widgets.Textarea(value='', layout=widgets.Layout(height="auto", width="100"))

        self.attachment1_label = Label("Att1", layout=Layout(display="flex", justify_content="center"))
        self.attachment1_name = Label("Att1", layout=Layout(display="flex", justify_content="center"))
        self.attachment1_load = widgets.Button(description='Select')

        # attachments
