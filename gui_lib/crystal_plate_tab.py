import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
import sqlalchemy as db
from shutil import move
from datetime import datetime
import os

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import crystal_plate_fs as fs
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query
import crystal_plate_db as db


class crystal_plate_tab(object):
    def __init__(self, settingsObject, dal, logger):

        self.settingsObject = settingsObject
        self.dal = dal
        self.logger = logger

        protein_history = [
            'frozen',
            'fresh'
        ]

        self.grid_widget_upper = widgets.GridspecLayout(13, 4)

#        self.grid_widget_upper[0,0] = Label("Enter New Barcode", layout=Layout(display="flex", justify_content="center"))
#        self.protein_concentration = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))

        self.grid_widget_upper[0, 0] = Label("Enter New Barcode")
        self.plate_barcode = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[0, 1] = self.plate_barcode
        add_plate_barcode_button = widgets.Button(description='Add')
        add_plate_barcode_button.on_click(self.add_plate_barcode)
        self.grid_widget_upper[0, 2] = add_plate_barcode_button

        self.grid_widget_upper[1, 0] = Label("Select Barcode")
        self.select_barcode = widgets.Dropdown(layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[1, 1] = self.select_barcode
        refresh_barcode_button = widgets.Button(description='Refresh Barcode List')
        refresh_barcode_button.on_click(self.refresh_barcode)
        self.grid_widget_upper[1, 2] = refresh_barcode_button

        self.grid_widget_upper[2, 0] = Label("Screen")
        self.select_screen_for_plate = widgets.Dropdown(layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[2, 1] = self.select_screen_for_plate
        refresh_screens_button = widgets.Button(description='Refresh Screen List')
        refresh_screens_button.on_click(self.refresh_screens)
        self.grid_widget_upper[2, 2] = refresh_screens_button

        load_plate_from_db_button = widgets.Button(description='Load Plate from DB', style= {'button_color':'orange'})
        load_plate_from_db_button.on_click(self.load_plate_from_db)
        self.grid_widget_upper[4:5, 2] = load_plate_from_db_button

        self.grid_widget_upper[3, 0] = Label("Protein Concentration (mg/ml)")
        self.protein_concentration = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[3, 1] = self.protein_concentration

        self.grid_widget_upper[4, 0] = Label("Protein Batch")
        self.select_protein_batch = widgets.Dropdown(layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[4, 1] = self.select_protein_batch

        self.grid_widget_upper[5, 0] = Label("Temperature (K)")
        self.temperature = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[5, 1] = self.temperature

        self.grid_widget_upper[6, 0] = Label("Protein Buffer")
        self.protein_buffer = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[6, 1] = self.protein_buffer

        self.grid_widget_upper[7, 0] = Label("Protein history")
        self.protein_history = widgets.Dropdown(layout=widgets.Layout(width="auto"))
        self.protein_history.options = protein_history
        self.grid_widget_upper[7, 1] = self.protein_history

        self.grid_widget_upper[8, 0] = Label("Reservoir Volume (\u03BCL)")
        self.reservoir_volume = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[8, 1] = self.reservoir_volume

        self.grid_widget_upper[9, 0] = Label("Plate Type")
        self.select_plate_type = widgets.Dropdown(layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[9, 1] = self.select_plate_type

        self.grid_widget_upper[10, 0] = Label("Method")
        self.select_method = widgets.Dropdown(layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[10, 1] = self.select_method

        self.grid_widget_upper[11, 0] = Label("start row")
        self.start_row = widgets.Text(value='A', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[11, 1] = self.start_row

        self.grid_widget_upper[11, 2] = Label("end row")
        self.end_row = widgets.Text(value='H', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[11, 3] = self.end_row

        self.grid_widget_upper[12, 0] = Label("start column")
        self.start_column = widgets.Text(value='01', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[12, 1] = self.start_column

        self.grid_widget_upper[12, 2] = Label("end column")
        self.end_column = widgets.Text(value='12', layout=widgets.Layout(width="auto"))
        self.grid_widget_upper[12, 3] = self.end_column

        file = open("images/swiss_ci_layout.png", "rb")
        image = file.read()
        swissci = widgets.Image(value=image, format='png', width=200, height=200)
#        self.grid_widget_upper[1:-1,-1] = swissci

        self.grid_widget_lower = widgets.GridspecLayout(11, 6)

        self.grid_widget_lower[0, :3] = widgets.Button(description="subwell 01", button_style="info", layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[1, 0] = widgets.Button(description="V(Protein) [nL]", button_style="info")
        self.grid_widget_lower[1, 1] = widgets.Button(description="V(Reservoir) [nL]", button_style="info")
        self.grid_widget_lower[1, 2] = widgets.Button(description="V(Seed) [nL]", button_style="info")
        self.subwell_a_protein = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[2, 0] = self.subwell_a_protein
        self.subwell_a_reservoir = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[2, 1] = self.subwell_a_reservoir
        self.subwell_a_seed = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[2, 2] = self.subwell_a_seed

        self.grid_widget_lower[3, :3] = widgets.Button(description="subwell 02", button_style="primary", layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[4, 0] = widgets.Button(description="V(Protein) [nL]", button_style="primary")
        self.grid_widget_lower[4, 1] = widgets.Button(description="V(Reservoir) [nL]", button_style="primary")
        self.grid_widget_lower[4, 2] = widgets.Button(description="V(Seed) [nL]", button_style="primary")
        self.subwell_c_protein = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[5, 0] = self.subwell_c_protein
        self.subwell_c_reservoir = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[5, 1] = self.subwell_c_reservoir
        self.subwell_c_seed = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[5, 2] = self.subwell_c_seed

        self.grid_widget_lower[6, :3] = widgets.Button(description="subwell 03", button_style="success", layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[7, 0] = widgets.Button(description="V(Protein) [nL]", button_style="success")
        self.grid_widget_lower[7, 1] = widgets.Button(description="V(Reservoir) [nL]", button_style="success")
        self.grid_widget_lower[7, 2] = widgets.Button(description="V(Seed) [nL]", button_style="success")
        self.subwell_d_protein = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[8, 0] = self.subwell_d_protein
        self.subwell_d_reservoir = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[8, 1] = self.subwell_d_reservoir
        self.subwell_d_seed = widgets.Text(layout=widgets.Layout(width="auto"))
        self.grid_widget_lower[8, 2] = self.subwell_d_seed

        save_plate_to_db_button = widgets.Button(description='Save CrystalPlate to Database',
                                          layout=widgets.Layout(height="auto", width="auto"),
                                           style= {'button_color':'gray'})
        save_plate_to_db_button.on_click(self.save_plate_to_db)
        self.grid_widget_lower[10, 0:] = save_plate_to_db_button
        self.grid_widget_lower[:9, 3:] = swissci


    def add_plate_barcode(self, b):
        l = []
        for opt in self.select_barcode.options: l.append(opt)
        if self.plate_barcode.value not in l:
            self.logger.info('adding ' + self.plate_barcode.value + ' to barcode dropdown')
            l.append(self.plate_barcode.value)
        else:
            self.logger.warning(self.plate_barcode.value + ' exists in screen dropdown')
        self.select_barcode.options = l

    def get_crystal_screen_from_db_for_dropdown(self):
        existing_crystalscreen = query.get_existing_crystal_screens_for_dropdown(self.dal, self.logger)
        self.select_screen_for_plate.options = existing_crystalscreen
        self.logger.info('updating screen selection dropdown: ' + str(existing_crystalscreen))

    def refresh_screens(self, b):
        self.get_crystal_screen_from_db_for_dropdown()

    def refresh_barcode(self, b):
        existing_crystalplates = query.get_existing_crystal_plate_barcodes(self.dal, self.logger)
        self.select_barcode.options = existing_crystalplates
        self.logger.info('updating barcode selection dropdown: ' + str(existing_crystalplates))


    def save_plate_to_db(self, b):
        self.logger.info('saving information for ' + self.select_barcode.value + ' to database')

        d = {}

        try:
            d['protein_batch_concentration'] = float(self.protein_concentration.value)
        except ValueError:
            d['protein_batch_concentration'] = 0.0

        d['protein_batch_concentration_unit'] = 'nL'

        try:
            d['temperature'] = float(self.temperature.value)
        except ValueError:
            d['temperature'] = 0.0

        try:
            d['reservoir_volume'] = float(self.reservoir_volume.value)
        except ValueError:
            d['reservoir_volume'] = 0.0

        d['reservoir_volume_unit'] = 'uL'

        try:
            d['subwell_01_protein_volume'] = float(self.subwell_a_protein.value)
        except ValueError:
            d['subwell_01_protein_volume'] = 0.0

        d['subwell_01_protein_volume_unit'] = 'nL'

        try:
            d['subwell_01_reservoir_volume'] = float(self.subwell_a_reservoir.value)
        except ValueError:
            d['subwell_01_reservoir_volume'] = 0.0

        d['subwell_01_reservoir_volume_unit'] = 'nL'

        try:
            d['subwell_01_seed_volume'] = float(self.subwell_a_seed.value)
        except ValueError:
            d['subwell_01_seed_volume'] = 0.0

        d['subwell_01_seed_volume_unit'] = 'nL'

        try:
            d['subwell_02_protein_volume'] = float(self.subwell_c_protein.value)
        except ValueError:
            d['subwell_02_protein_volume'] = 0.0

        d['subwell_02_protein_volume_unit'] = 'nL'

        try:
            d['subwell_02_reservoir_volume'] = float(self.subwell_c_reservoir.value)
        except ValueError:
            d['subwell_02_reservoir_volume'] = 0.0

        d['subwell_02_reservoir_volume_unit'] = 'nL'

        try:
            d['subwell_02_seed_volume'] = float(self.subwell_c_seed.value)
        except ValueError:
            d['subwell_02_seed_volume'] = 0.0

        d['subwell_02_seed_volume_unit'] = 'nL'

        try:
            d['subwell_03_protein_volume'] = float(self.subwell_d_protein.value)
        except ValueError:
            d['subwell_03_protein_volume'] = 0.0

        d['subwell_03_protein_volume_unit'] = 'nL'

        try:
            d['subwell_03_reservoir_volume'] = float(self.subwell_d_reservoir.value)
        except ValueError:
            d['subwell_03_reservoir_volume'] = 0.0

        d['subwell_03_reservoir_volume_unit'] = 'nL'

        try:
            d['subwell_03_seed_volume'] = float(self.subwell_d_seed.value)
        except ValueError:
            d['subwell_03_seed_volume'] = 0.0

        d['subwell_03_seed_volume_unit'] = 'nL'

        d['protein_batch_id'] = self.select_protein_batch.value.split(':')[0]
        d['protein_batch_buffer'] = self.protein_buffer.value
        d['crystallization_method_id'] = self.select_method.value.split(':')[0]
        d['plate_type_id'] = self.select_plate_type.value.split(':')[0]
        d['crystal_screen_id'] = self.select_screen_for_plate.value.split(':')[0]
        d['protein_history'] = self.protein_history.value

        d['start_row'] = self.start_row.value
        d['end_row'] = self.end_row.value
        d['start_column'] = self.start_column.value
        d['end_column'] = self.end_column.value

        barcode = self.select_barcode.value

        db.save_crystal_plate_to_database(self.logger, self.dal, d, barcode)

#        fs.save_shifter_csv_to_inspect_folder(self.logger,
#                                              d['subwell_01_protein_volume'],
#                                              d['subwell_02_protein_volume'],
#                                              d['subwell_03_protein_volume'],
#                                              self.select_barcode.value,
#                                              self.select_plate_type.value.split(':')[1].replace(' ', ''),
#                                              self.settingsObject.workflow_folder)

        fs.save_crystal_plate_csv_to_inspect_folder(self.logger,
                                                    d['subwell_01_protein_volume'],
                                                    d['subwell_02_protein_volume'],
                                                    d['subwell_03_protein_volume'],
                                                    self.select_barcode.value,
                                                    self.select_plate_type.value.split(':')[1].replace(' ', ''),
                                                    self.settingsObject.workflow_folder,
                                                    d['start_row'],
                                                    d['end_row'],
                                                    d['start_column'],
                                                    d['end_column'])

    def load_plate_from_db(self, b):
        x = db.load_crystal_plate_from_database(self.dal, self.logger, self.select_barcode.value)
        self.reservoir_volume.value = str(x['reservoir_volume'])
        self.protein_concentration.value = str(x['protein_batch_concentration'])
        self.temperature.value = str(x['temperature'])
        self.subwell_a_protein.value = str(x['subwell_a_protein_volume'])
        self.subwell_a_reservoir.value = str(x['subwell_a_reservoir_volume'])
        self.subwell_a_seed.value = str(x['subwell_a_seed_volume'])
        self.subwell_c_protein.value = str(x['subwell_c_protein_volume'])
        self.subwell_c_reservoir.value = str(x['subwell_c_reservoir_volume'])
        self.subwell_c_seed.value = str(x['subwell_c_seed_volume'])
        self.subwell_d_protein.value = str(x['subwell_d_protein_volume'])
        self.subwell_d_reservoir.value = str(x['subwell_d_reservoir_volume'])
        self.subwell_d_seed.value = str(x['subwell_d_seed_volume'])
        self.protein_buffer.value = str(x['protein_batch_buffer'])

        crystal_screen_id = x['crystal_screen_id']

        self.get_crystal_screen_from_db_for_dropdown()
        for option in self.select_screen_for_plate.options:
            if int(option.split(':')[0]) == crystal_screen_id:
                self.select_screen_for_plate.value = option
                break

