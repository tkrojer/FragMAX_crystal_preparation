import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from tkinter import Tk, filedialog
from IPython.display import display,clear_output

import os, sys

sys.path.append(os.path.join(os.getcwd(), 'lib'))
from init_filesystem import init_filesystem
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import prep_tables
import query
import project_db as db

#import sqlalchemy as db
#from shutil import copyfile
#from shutil import move
#from datetime import datetime
#import sqlite3
#import csv

class project_tab(object):
    def __init__(self, settingsObject, logger, dal, standard_table_file, crystalplateObject, soakplateObject):

        self.settings = settingsObject
        self.crystalplateObject = crystalplateObject
        self.soakplateObject = soakplateObject
        self.logger = logger
        self.dal = dal
        self.standard_table_file = standard_table_file

        self.grid_widget = widgets.GridspecLayout(6, 4)

        self.grid_widget[0, 0] = Label("Project Name", layout=Layout(display="flex", justify_content="center"))
        self.project_name = widgets.Text(value='', layout=widgets.Layout(height="auto", width="200"))
        self.grid_widget[0, 1:] = self.project_name

        self.grid_widget[1, 0] = Label("Proposal ID", layout=Layout(display="flex", justify_content="center"))
        self.proposal_id = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[1, 1:] = self.proposal_id

        self.grid_widget[2, 0] = Label("Protein Name", layout=Layout(display="flex", justify_content="center"))
        self.protein_name = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[2, 1:] = self.protein_name

        self.grid_widget[3, 0] = Label("Protein Acronym", layout=Layout(display="flex", justify_content="center"))
        self.protein_acronym = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[3, 1:] = self.protein_acronym

        self.grid_widget[4, 0] = Label("Project Directory", layout=Layout(display="flex", justify_content="center"))
        self.project_directory = widgets.Text(value='', layout=widgets.Layout(height="auto", width="200"))
        self.grid_widget[4, 1:2] = self.project_directory
        self.select_project_directory_button = widgets.Button(description='Select',
                                                                    style={'button_color': 'green'})
        self.select_project_directory_button.on_click(self.select_project_directory)
        self.grid_widget[4, 3] = self.select_project_directory_button

        self.read_project_button = widgets.Button(description='Read from DB')
        self.read_project_button.on_click(self.read_project)
        self.grid_widget[5,0] = self.read_project_button

        self.save_project_button = widgets.Button(description='Save to DB')
        self.save_project_button.on_click(self.save_project)
        self.grid_widget[5,1] = self.save_project_button

    def select_project_directory(self, b):
        clear_output()  # Button is deleted after it is clicked.
        root = Tk()
        root.withdraw()  # Hide the main window.
        root.call('wm', 'attributes', '.', '-topmost', True)  # Raise the root to the top of all windows.
#        b.folder = filedialog.askdirectory(initialdir=self.lp3_project_folder, title="Select project directory")
        b.folder = filedialog.askdirectory(title="Select project directory")

        if os.path.isdir(b.folder):
            self.settings.project_folder = b.folder
            init_filesystem(self.settings, self.logger).init_folders()
            init_filesystem(self.settings, self.logger).init_db(self.dal)
            prep_tables.insert(self.dal, self.standard_table_file, self.logger)
            self.project_directory.value = str(self.settings.project_folder)
            self.read_project_from_db()
        else:
            self.logger.error('selected project folder does not exist: ' + str(b.folder))

    def read_project(self, b):
        self.read_project_from_db()

    def read_project_from_db(self):
        self.logger.info('reading project information from database')
        d = db.get_project_info(self.dal, self.logger)
        self.update_project_widgets(d)
        self.update_crystal_plate_widgets()

    def update_project_widgets(self, d):
        self.logger.info('updating fields in project description tab')
        self.project_name.value = str(d['project_name'])
        self.proposal_id.value = str(d['proposal_number'])
        self.protein_name.value = str(d['protein_name'])
        self.protein_acronym.value = str(d['protein_acronym'])

    def save_project(self, b):
        self.logger.info('saving project information to database')
        d = {
            'project_id': 1,
            'project_name': self.project_name.value,
            'proposal_number': self.proposal_id.value.replace(' ', ''),
            'protein_name': self.protein_name.value,
            'protein_acronym': self.protein_acronym.value.replace(' ', ''),
            'project_directory': self.project_directory.value
        }
        db.save_project_info(self.dal, self.logger, d)
        self.update_crystal_plate_widgets()

    def update_crystal_plate_widgets(self):
        existing_protein_batches = query.get_protein_batch_for_dropdown(self.dal, self.logger)
        self.logger.info('found the following protein batches in database: ' + str(existing_protein_batches))
        self.crystalplateObject.select_protein_batch.options = existing_protein_batches

        existing_plate_types = query.get_plate_type_for_dropdown(self.dal, self.logger)
        self.logger.info('found the following crystal plate types in database: ' + str(existing_plate_types))
        self.crystalplateObject.select_plate_type.options = existing_plate_types

        existing_methods = query.get_crystallization_method_for_dropdown(self.dal, self.logger)
        self.logger.info('found the following crystallization methods in database: ' + str(existing_methods))
        self.crystalplateObject.select_method.options = existing_methods
