import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label

class page_header(object):
    def __init__(self):
        file = open("images/FragMAX-logo-full.png", "rb")
        image = file.read()
        FragMAX = widgets.Image(value=image, format='png', width=200, height=300)

        #title = widgets.Label(value='Crystal Plate Preparation')
        text = 'Crystal Preparation'
        title = widgets.HTML(value = f"<b><font color='black'><font size = 10px>{text}</b>")

        text = 'XX'
        spacer = widgets.HTML(value = f"<b><font color='white'><font size = 6px>{text}</b>")

        self.logo = HBox(children=[FragMAX, spacer, title],layout=Layout(width='100%', display='flex', align_items='center'))