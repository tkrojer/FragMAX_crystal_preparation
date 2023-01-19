from ipywidgets import widgets
from IPython.display import Javascript, display, clear_output

notify_output = widgets.Output()
display(notify_output)

@notify_output.capture()
def popup(text):
    clear_output()
    display(Javascript("alert('{}')".format(text)))
