import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
import qgrid
from shutil import copyfile
from tkinter import Tk, filedialog
import ntpath
#import sqlalchemy as db
import os
import csv
import pandas as pd

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import crystal_screen_fs as fs
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query
import crystal_screen_db as db


class crystal_screen_tab(object):
    def __init__(self, settingsObject, dal, logger, crystal_plate_template, progress_bar):

        self.settings = settingsObject
        self.dal = dal
        self.logger = logger
        self.crystal_plate_template = crystal_plate_template
        self.progress_bar = progress_bar

        self.grid_widget = widgets.GridspecLayout(3, 4)

        self.grid_widget[0, 0] = Label("Enter New Screen Name", layout=Layout(display="flex", justify_content="center"))

        self.screen_name = widgets.Text(value='', layout=widgets.Layout(height="auto", width="auto"))
        self.grid_widget[0, 1] = self.screen_name
        self.add_screen_button = widgets.Button(description='Add')
        self.add_screen_button.on_click(self.add_screen)
        self.grid_widget[0, 2] = self.add_screen_button
        self.grid_widget[1, 0] = Label("Select Screen", layout=Layout(display="flex", justify_content="center"))
        self.select_screen = widgets.Dropdown()
        self.grid_widget[1, 1] = self.select_screen

        self.refresh_screen_button = widgets.Button(description='Refresh Screen List')
        self.refresh_screen_button.on_click(self.refresh_screen_dropdown)
        self.grid_widget[1, 2] = self.refresh_screen_button

        self.load_selected_screen_button = widgets.Button(description="Load Screen from DB",
                                                     layout=widgets.Layout(height="auto", width="auto"))
        self.load_selected_screen_button.on_click(self.load_screen_from_db)
        self.grid_widget[2, 0] = self.load_selected_screen_button

        save_screen_excel_button = widgets.Button(description="Save EXCEL template",
                                                layout=widgets.Layout(height="auto", width="auto"))
        save_screen_excel_button.on_click(self.save_screen_excel)
        self.grid_widget[2, 1] = save_screen_excel_button

        upload_screen_excel_button = widgets.Button(description="Upload EXCEL file",
                                                  layout=widgets.Layout(height="auto", width="auto"))
        upload_screen_excel_button.on_click(self.upload_screen_excel)
        self.grid_widget[2, 2] = upload_screen_excel_button

        self.import_dragonfly_button = widgets.Button(description="Import Dragonfly file",
                                                 layout=widgets.Layout(height="auto", width="auto"))
        self.import_dragonfly_button.on_click(self.import_dragonfly)
        self.grid_widget[2, 3] = self.import_dragonfly_button

        df_template = pd.read_csv(self.crystal_plate_template)
        self.screen_sheet = qgrid.QgridWidget(df=df_template, show_toolbar=False)

        self.save_screen_to_db_button = widgets.Button(description='Save CrystalScreen to Database',
                                                  layout=widgets.Layout(height="auto", width="auto"),
                                                  style={'button_color': 'gray'})
        self.save_screen_to_db_button.on_click(self.save_screen_to_db)

#        self.crystal_screen_progress = IntProgress(min=0, max=95)

    def add_screen(self, b):
        self.add_screen_to_dropdown()

    def add_screen_to_dropdown(self):
        l = []
        for opt in self.select_screen.options: l.append(opt)
        if self.screen_name.value not in l:
            self.logger.info('adding ' + self.screen_name.value + ' to screen dropdown')
            l.append((self.screen_name.value, None))
        else:
            self.logger.warning(self.screen_name.value + ' exists in screen dropdown')
        self.select_screen.options = l

    def refresh_screen_dropdown(self, b):
        existing_crystalscreens = query.get_existing_crystal_screens_for_dropdown(self.dal, self.logger)
        self.select_screen.options = existing_crystalscreens
        self.logger.info('updating screen selection dropdown: ' + str(existing_crystalscreens))

    def load_screen_from_db(self, b):
        existing_crystalscreens = query.get_existing_crystal_screens_for_dropdown(self.dal, self.logger)
        if self.select_screen.value in existing_crystalscreens:
            self.logger.info('screen ' + self.select_screen.value + ' exists in database')
            df = db.get_crystal_screen_conditions_as_df(self.dal, self.logger, self.select_screen.value)
            self.screen_sheet.df = df
        else:
            self.logger.warning('screen {0!s} does not exist in database; skipping...'.format(self.select_screen.value))

#    def save_screen_csv(self, b):
#        crystal_screen_name = self.select_screen.value.replace(' ','')
#        fs.save_crystal_screen_as_excel(self.logger, self.settings.crystal_screen_folder,
#                                        crystal_screen_name, self.crystal_plate_template)

    def save_screen_excel(self, b):
        crystal_screen_name = self.select_screen.label.replace(' ','')
        fs.save_crystal_screen_as_excel(self.logger, self.settings.crystal_screen_folder,
                                        crystal_screen_name, self.crystal_plate_template)


    def upload_screen_excel(self, b):
        clear_output()
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        b.files = filedialog.askopenfilename(multiple=True,
                                             initialdir=os.path.join(self.settings.project_folder, 'crystal_screen'),
                                             title="Select file",
                                             filetypes=[("Excel files", "*.xlsx")])
        if os.path.isfile(b.files[0]):
            self.logger.info('loading ' + b.files[0])
            self.screen_name.value = ntpath.basename(b.files[0]).split('.')[0]
            self.add_screen_to_dropdown()
#            dialect = csv.Sniffer().sniff(open(b.files[0]).readline(), [',', ';'])
#            df = pd.read_csv(b.files[0], sep=dialect.delimiter)
            self.screen_sheet.df = fs.read_crystal_screen_as_df(self.logger, b.files[0])
        else:
            self.logger.error('cannot read file ' + b.files[0])


    def save_dragonfly_to_csv(self, dragonflyFile):
        fs.save_dragonfly_to_csv(self.logger, dragonflyFile)


    def import_dragonfly(self, b):
        clear_output()  # Button is deleted after it is clicked.
        root = Tk()
        root.withdraw()  # Hide the main window.
        root.call('wm', 'attributes', '.', '-topmost', True)  # Raise the root to the top of all windows.
        b.files = filedialog.askopenfilename(multiple=True,
                                             initialdir=self.settings.crystal_screen_folder,
                                             title="Select dragonfly file",
                                             filetypes=[("Text Files",
                                                         "*.txt")])  # List of selected files will be set button's file attribute.

        if os.path.isfile(b.files[0]):
            self.screen_name.value = ntpath.basename(b.files[0]).split('.')[0]
            self.add_screen_to_dropdown()
            self.save_dragonfly_to_csv(b.files[0])
            dragonflyCSV = b.files[0].replace('.txt', '.csv')
            self.logger.info('loading ' + dragonflyCSV)
            df = pd.read_csv(dragonflyCSV, sep=',')
            self.screen_sheet.df = df


    def save_screen_to_db(self, b):
        df = self.screen_sheet.get_changed_df()
        csname = self.select_screen.label.replace(' ','')
#        csid = self.select_screen.value
        db.save_crystal_screen_to_db(self.dal, self.logger, df, csname, self.progress_bar)

