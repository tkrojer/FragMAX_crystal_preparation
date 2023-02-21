import ipywidgets as widgets
from tkinter import Tk, filedialog
from IPython.display import display,clear_output
import os
import glob
from shutil import (copyfile, move)
from datetime import datetime

import log

class gui(object):
    def __init__(self, settingsObject, logger):
        self.settingsObject = settingsObject
        self.logger = logger

        self.grid_widget = widgets.GridspecLayout(10, 3)

        height = '80px'

        self.button_01 = widgets.Button(description='01', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_02 = widgets.Button(description='02', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_03 = widgets.Button(description='03', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_04 = widgets.Button(description='04', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_05 = widgets.Button(description='05', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_06 = widgets.Button(description='06', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_07 = widgets.Button(description='07', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_08 = widgets.Button(description='08', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_09 = widgets.Button(description='09', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_10 = widgets.Button(description='10', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})
        self.button_11 = widgets.Button(description='11', layout=widgets.Layout(width="auto", height=height),
                                        style={'button_color': 'lightgray'})

        self.button_01.on_click(self.set_scan_value_button)
        self.button_02.on_click(self.set_scan_value_button)
        self.button_03.on_click(self.set_scan_value_button)
        self.button_04.on_click(self.set_scan_value_button)
        self.button_05.on_click(self.set_scan_value_button)
        self.button_06.on_click(self.set_scan_value_button)
        self.button_07.on_click(self.set_scan_value_button)
        self.button_08.on_click(self.set_scan_value_button)
        self.button_09.on_click(self.set_scan_value_button)
        self.button_10.on_click(self.set_scan_value_button)
        self.button_11.on_click(self.set_scan_value_button)

        self.grid_widget[0, 0] = self.button_10
        self.grid_widget[0, 1] = self.button_11
        self.grid_widget[1, 0] = self.button_07
        self.grid_widget[1, 1] = self.button_08
        self.grid_widget[1, 2] = self.button_09
        self.grid_widget[2, 0] = self.button_04
        self.grid_widget[2, 1] = self.button_05
        self.grid_widget[2, 2] = self.button_06
        self.grid_widget[3, 0] = self.button_01
        self.grid_widget[3, 1] = self.button_02
        self.grid_widget[3, 2] = self.button_03

        self.settingsObject.rack_dict['01'] = self.button_01
        self.settingsObject.rack_dict['02'] = self.button_02
        self.settingsObject.rack_dict['03'] = self.button_03
        self.settingsObject.rack_dict['04'] = self.button_04
        self.settingsObject.rack_dict['05'] = self.button_05
        self.settingsObject.rack_dict['06'] = self.button_06
        self.settingsObject.rack_dict['07'] = self.button_07
        self.settingsObject.rack_dict['08'] = self.button_08
        self.settingsObject.rack_dict['09'] = self.button_09
        self.settingsObject.rack_dict['10'] = self.button_10
        self.settingsObject.rack_dict['11'] = self.button_11

        self.grid_widget[5, 0] = widgets.Label("scan or type",
                                               layout=widgets.Layout(display="flex", justify_content="center"))
        self.scan_value = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget[5, 1] = self.scan_value
        clear_scan = widgets.Button(description='clear', layout=widgets.Layout(width="auto"))
        clear_scan.on_click(self.clear_scan_value)
        self.grid_widget[5, 2] = clear_scan

        reset_button = widgets.Button(description='reset', layout=widgets.Layout(width="auto"))
        reset_button.on_click(self.reset_all_fields)
        self.grid_widget[6, 0] = reset_button

        self.type = widgets.Dropdown(layout=widgets.Layout(width="auto"))
        self.type.options = self.settingsObject.plate_types
        self.grid_widget[6, 1] = self.type

        self.tip_start = widgets.Text(value='A1', layout=widgets.Layout(width="auto"))
        self.grid_widget[6, 2] = self.tip_start

        load_project_button = widgets.Button(description='load project', layout=widgets.Layout(width="auto"))
        load_project_button.on_click(self.select_project_directory)
        self.grid_widget[7, 0] = load_project_button

    def select_project_directory(self, b):
        clear_output()  # Button is deleted after it is clicked.
        root = Tk()
        root.withdraw()  # Hide the main window.
        root.call('wm', 'attributes', '.', '-topmost', True)  # Raise the root to the top of all windows.
        b.folder = filedialog.askdirectory(title="Select project directory")
        self.init_logger(b.folder)

    def init_logger(self, folder):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.settingsObject.project_folder = folder
        self.settingsObject.workflow_folder = os.path.join(self.settingsObject.project_folder, 'workflow')
        self.settingsObject.logfile_folder = os.path.join(self.settingsObject.project_folder, 'log')
        logfile = os.path.join(self.settingsObject.logfile_folder, 'opentrons.log')
        if os.path.isfile(logfile):
            move(logfile, os.path.join(os.path.join(self.settingsObject.logfile_folder, 'backup', 'opentrons.log.' + now)))
        self.logger = log.init_logger(self.logger, os.path.join(self.settingsObject.logfile_folder, 'opentrons.log'))
        self.logger.info('starting new session...')
        self.logger.info('project directory: ' + self.settingsObject.project_folder)
        self.logger.info('log directory: ' + self.settingsObject.logfile_folder)
        self.logger.info('workflow directory: ' + self.settingsObject.workflow_folder)

    def clear_scan_value(self, b):
        self.scan_value.value = ''

    def set_scan_value_button(self, b):
        self.update_button_and_fields(b)

    def barcode_exists(self, ext):
        exists = False
        self.logger.info('searching for plates in ' + os.path.join(self.settingsObject.workflow_folder, '2-soak'))
        if os.path.isfile(os.path.join(self.settingsObject.workflow_folder, '2-soak', self.scan_value.value + ext)):
            exists = True
            self.logger.info('found {0!s}: {1!s}'.format(self.type.value, self.scan_value.value + ext))
        else:
            self.logger.error('cannot find {0!s}: {1!s}'.format(self.type.value, self.scan_value.value + ext))
        return exists

    def check_if_type_assigned(self):
        for key in self.settingsObject.rack_dict:
            if self.settingsObject.rack_dict[key].description.startswith(self.type.value):
                self.settingsObject.rack_dict[key].description = key
                self.settingsObject.rack_dict[key].style.button_color = 'lightgray'

    def update_button_and_fields(self, button):
        self.logger.info('setting button {0!s} to {1!s}'.format(button.description, self.scan_value.value))
        if self.type.value.startswith('tip'):
            if self.type.value.endswith('2') and self.tip_start.value != 'A1':
                self.logger.error('tip rack 2 must be full, starting at position A1')
            else:
                self.check_if_type_assigned()
                button.description = self.type.value + ' - ' + self.tip_start.value
                button.style.button_color = 'yellow'
        elif self.type.value.startswith('compound'):
            if self.barcode_exists('_soak.csv'):
                self.check_if_type_assigned()
                button.description = self.type.value + ' - ' + self.scan_value.value
                button.style.button_color = 'cyan'
        elif self.type.value.startswith('target'):
            if self.barcode_exists('_xtal.csv'):
                self.check_if_type_assigned()
                button.description = self.type.value + ' - ' + self.scan_value.value
                button.style.button_color = 'orange'
        else:
            self.logger.error('unknown error')

    def reset_all_fields(self, b):
        self.logger.info('resetting all button')
        self.scan_value.value = ''
        for key in self.settingsObject.rack_dict:
            self.settingsObject.rack_dict[key].description = key
            self.settingsObject.rack_dict[key].style.button_color = 'lightgray'

