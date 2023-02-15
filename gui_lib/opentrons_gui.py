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
        self.plate_dict = {'crystal_plate': [], 'soak_plate': []}

        self.grid_widget = widgets.GridspecLayout(9, 3)
        self.button_01 = widgets.Button(description='01', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_02 = widgets.Button(description='02', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_03 = widgets.Button(description='03', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_04 = widgets.Button(description='04', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_05 = widgets.Button(description='05', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_06 = widgets.Button(description='06', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_07 = widgets.Button(description='07', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_08 = widgets.Button(description='08', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_09 = widgets.Button(description='09', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_10 = widgets.Button(description='10', layout=widgets.Layout(width="auto"),
                                        style={'button_color': 'lightgray'})
        self.button_11 = widgets.Button(description='11', layout=widgets.Layout(width="auto"),
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

        self.grid_widget[5, 0] = widgets.Label("scan", layout=widgets.Layout(display="flex", justify_content="center"))
        self.scan_value = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget[5, 1] = self.scan_value
        clear_scan = widgets.Button(description='clear', layout=widgets.Layout(width="auto"))
        clear_scan.on_click(self.clear_scan_value)
        self.grid_widget[5, 2] = clear_scan

        reset_button = widgets.Button(description='reset', layout=widgets.Layout(width="auto"))
        reset_button.on_click(self.reset_all_fields)
        self.grid_widget[6, 0] = reset_button

        add_tips_button = widgets.Button(description='tip rack', layout=widgets.Layout(width="auto"))
        add_tips_button.on_click(self.add_tips)
        self.grid_widget[6, 1] = add_tips_button

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
        self.settingsObject.project_folder = b.folder
        self.settingsObject.workflow_folder = os.path.join(self.settingsObject.project_folder, 'workflow')
        self.settingsObject.logfile_folder = os.path.join(self.settingsObject.project_folder, 'log')
        self.init_logger()
        self.plate_dict = {'crystal_plate': [], 'soak_plate': []}
        for f in glob.glob(os.path.join(self.settingsObject.workflow_folder, '2-soak', '*.csv')):
            if f.endswith('_xtal.csv'):
                self.logger.info('found crystal plate: {0!s}'.format(os.path.basename(f)))
                self.plate_dict['crystal_plate'].append(os.path.basename(f).replace('.csv', ''))
            if f.endswith('_soak.csv'):
                self.logger.info('found soak plate: {0!s}'.format(os.path.basename(f)))
                self.plate_dict['soak_plate'].append(os.path.basename(f).replace('.csv', ''))

    def init_logger(self):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
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

    def update_button_and_fields(self, button):
        self.logger.info('setting button {0!s} to {1!s}'.format(button.description, self.scan_value.value))
        if self.scan_value.value.startswith('tips rack'):
            button.style.button_color = 'lime'
            button.description = self.scan_value.value
        else:
            plate_type = self.get_plate_type()
            if plate_type == 'crystal_plate':
                button.description = self.scan_value.value
                button.style.button_color = 'orange'
            elif plate_type == 'soak_plate':
                button.description = self.scan_value.value
                button.style.button_color = 'cyan'
            else:
                print('error')
#                self.logger.error('plate does not exist in {0!s}'.format(os.path.join(self.settingsObject.workflow_folder, '2-soak')))

    def get_plate_type(self):
        plate_type = None
        for key in self.plate_dict:
            for item in self.plate_dict[key]:
                print(item, self.scan_value.value)
                if item == self.scan_value.value:
                    plate_type = key
        return plate_type

    def reset_all_fields(self, b):
        self.logger.info('resetting all button')
        self.scan_value.value = ''
        self.button_01.description = '01'
        self.button_01.style.button_color = 'lightgray'
        self.button_02.description = '02'
        self.button_02.style.button_color = 'lightgray'
        self.button_03.description = '03'
        self.button_03.style.button_color = 'lightgray'
        self.button_04.description = '04'
        self.button_04.style.button_color = 'lightgray'
        self.button_05.description = '05'
        self.button_05.style.button_color = 'lightgray'
        self.button_06.description = '06'
        self.button_06.style.button_color = 'lightgray'
        self.button_07.description = '07'
        self.button_07.style.button_color = 'lightgray'
        self.button_08.description = '08'
        self.button_08.style.button_color = 'lightgray'
        self.button_09.description = '09'
        self.button_09.style.button_color = 'lightgray'
        self.button_10.description = '10'
        self.button_10.style.button_color = 'lightgray'
        self.button_11.description = '11'
        self.button_11.style.button_color = 'lightgray'

    def add_tips(self, b):
        self.scan_value.value = 'tips rack - {0!s}'.format(self.tip_start.value.replace(' ', ''))

