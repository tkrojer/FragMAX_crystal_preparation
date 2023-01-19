import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
import sqlalchemy as db
from shutil import move
from datetime import datetime
import os

import sys
#sys.path.append(os.path.join(os.getcwd(), 'lib'))
#import filesystem as fs
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query


class crystal_plate_tab(object):
    def __init__(self, settingsObject, dal, logger):

        self.settingsObject = settingsObject
        self.dal = dal
        self.logger = logger

        self.grid_widget_upper = widgets.GridspecLayout(10, 4)

        self.grid_widget_upper[0,0] = Label("Enter New Barcode", layout=Layout(display="flex", justify_content="center"))

        self.plate_barcode = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_upper[0,1] = self.plate_barcode
        add_plate_barcode_button = widgets.Button(description='Add')
        add_plate_barcode_button.on_click(self.add_plate_barcode)
        self.grid_widget_upper[0,2] = add_plate_barcode_button

        self.grid_widget_upper[1,0] = Label("Select Barcode", layout=Layout(display="flex", justify_content="center"))
        self.select_barcode = widgets.Dropdown()
        self.grid_widget_upper[1,1] = self.select_barcode
        refresh_barcode_button = widgets.Button(description='Refresh Barcode List')
        refresh_barcode_button.on_click(self.refresh_barcode)
        self.grid_widget_upper[1,2] = refresh_barcode_button

        self.grid_widget_upper[2,0] = Label("Screen", layout=Layout(display="flex", justify_content="center"))
        self.select_screen_for_plate = widgets.Dropdown()
        self.grid_widget_upper[2,1] = self.select_screen_for_plate
        refresh_screens_button = widgets.Button(description='Refresh Screen List')
        refresh_screens_button.on_click(self.refresh_screens)
        self.grid_widget_upper[2,2] = refresh_screens_button

        load_plate_from_db_button = widgets.Button(description='Load Plate from DB', style= {'button_color':'orange'})
        load_plate_from_db_button.on_click(self.load_plate_from_db)
        self.grid_widget_upper[4:5,2] = load_plate_from_db_button

        self.grid_widget_upper[3,0] = Label("Protein Concentration (mg/ml)", layout=Layout(display="flex", justify_content="center"))
        self.protein_concentration = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_upper[3,1] = self.protein_concentration

        self.grid_widget_upper[4,0] = Label("Protein Batch", layout=Layout(display="flex", justify_content="center"))
        self.select_protein_batch = widgets.Dropdown()
        self.grid_widget_upper[4,1] = self.select_protein_batch

        self.grid_widget_upper[5,0] = Label("Temperature (K)", layout=Layout(display="flex", justify_content="center"))
        self.temperature = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_upper[5,1] = self.temperature

        self.grid_widget_upper[6,0] = Label("Protein Buffer", layout=Layout(display="flex", justify_content="center"))
        self.protein_buffer = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_upper[6,1] = self.protein_buffer

        self.grid_widget_upper[7,0] = Label("Reservoir Volume (\u03BCL)", layout=Layout(display="flex", justify_content="center"))
        self.reservoir_volume = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_upper[7,1] = self.reservoir_volume

        self.grid_widget_upper[8,0] = Label("Plate Type", layout=Layout(display="flex", justify_content="center"))
        self.select_plate_type = widgets.Dropdown()
        self.grid_widget_upper[8,1] = self.select_plate_type

        self.grid_widget_upper[9,0] = Label("Method", layout=Layout(display="flex", justify_content="center"))
        self.select_method = widgets.Dropdown()
        self.grid_widget_upper[9,1] = self.select_method

        file = open("images/swiss_ci_layout.png", "rb")
        image = file.read()
        swissci = widgets.Image(value=image, format='png', width=200, height=200)
        self.grid_widget_upper[1:-1,-1] = swissci

        self.grid_widget_lower = widgets.GridspecLayout(11, 3)

        self.grid_widget_lower[0,0:] = widgets.Button(description="subwell a", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="info")
        self.grid_widget_lower[1,0] = widgets.Button(description="V(Protein) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="info")
        self.grid_widget_lower[1,1] = widgets.Button(description="V(Reservoir) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="info")
        self.grid_widget_lower[1,2] = widgets.Button(description="V(Seed) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="info")
        self.subwell_a_protein = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[2,0] = self.subwell_a_protein
        self.subwell_a_reservoir = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[2,1] = self.subwell_a_reservoir
        self.subwell_a_seed = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[2,2] = self.subwell_a_seed

        self.grid_widget_lower[3,0:] = widgets.Button(description="subwell c", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="primary")
        self.grid_widget_lower[4,0] = widgets.Button(description="V(Protein) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="primary")
        self.grid_widget_lower[4,1] = widgets.Button(description="V(Reservoir) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="primary")
        self.grid_widget_lower[4,2] = widgets.Button(description="V(Seed) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="primary")
        self.subwell_c_protein = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[5,0] = self.subwell_c_protein
        self.subwell_c_reservoir = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[5,1] = self.subwell_c_reservoir
        self.subwell_c_seed = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[5,2] = self.subwell_c_seed

        self.grid_widget_lower[6,0:] = widgets.Button(description="subwell d", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="success")
        self.grid_widget_lower[7,0] = widgets.Button(description="V(Protein) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="success")
        self.grid_widget_lower[7,1] = widgets.Button(description="V(Reservoir) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="success")
        self.grid_widget_lower[7,2] = widgets.Button(description="V(Seed) [nL]", layout=widgets.Layout(height="auto", width="auto"),
                            button_style="success")

        self.subwell_d_protein = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[8,0] = self.subwell_d_protein
        self.subwell_d_reservoir = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[8,1] = self.subwell_d_reservoir
        self.subwell_d_seed = widgets.Text(layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget_lower[8,2] = self.subwell_d_seed

        save_plate_to_db_button = widgets.Button(description='Save CrystalPlate to Database',
                                          layout=widgets.Layout(height="auto", width="auto"),
                                           style= {'button_color':'gray'})
        save_plate_to_db_button.on_click(self.save_plate_to_db)
        self.grid_widget_lower[10,0:] = save_plate_to_db_button


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
#        query = db.select([self.dbObject.crystalscreenTable.columns.CrystalScreen_Name.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        existing_crystalscreen = [x[0] for x in ResultProxy.fetchall()]
#        existing_crystalscreen = query.get_existing_crystal_screens_for_dropdown(self.dal, self.logger)
#        self.select_screen_for_plate.options = existing_crystalscreen
#        self.logger.info('updating screen selection dropdown: ' + str(existing_crystalscreen))
        self.get_crystal_screen_from_db_for_dropdown()

    def refresh_barcode(self, b):
#        query = db.select([self.dbObject.crystalplateTable.columns.CrystalPlate_Barcode.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        existing_crystalplates = [x[0] for x in ResultProxy.fetchall()]
        existing_crystalplates = query.get_existing_crystal_plate_barcodes(self.dal, self.logger)
        self.select_barcode.options = existing_crystalplates
        self.logger.info('updating barcode selection dropdown: ' + str(existing_crystalplates))


    def save_plate_to_db(self, b):
        self.logger.info('saving information for ' + self.select_barcode.value + ' to database')
#        query = db.select([self.dbObject.crystalplateTable.columns.CrystalPlate_Barcode.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        existing_barcodes = [x[0] for x in ResultProxy.fetchall()]

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
            d['subwell_a_protein_volume'] = float(self.subwell_a_protein.value)
        except ValueError:
            d['subwell_a_protein_volume'] = 0.0

        d['subwell_a_protein_volume'] = 'nL'

        try:
            d['subwell_a_reservoir_volume'] = float(self.subwell_a_reservoir.value)
        except ValueError:
            d['subwell_a_reservoir_volume'] = 0.0

        d['subwell_a_reservoir_volume_unit'] = 'nL'

        try:
            d['subwell_a_seed_volume'] = float(self.subwell_a_seed.value)
        except ValueError:
            d['subwell_a_seed_volume'] = 0.0

        d['subwell_a_seed_volume_unit'] = 'nL'

        try:
            d['subwell_c_protein_volume'] = float(self.subwell_c_protein.value)
        except ValueError:
            d['subwell_c_protein_volume'] = 0.0

        d['subwell_c_protein_volume_unit'] = 'nL'

        try:
            d['subwell_c_reservoir_volume'] = float(self.subwell_c_reservoir.value)
        except ValueError:
            d['subwell_c_reservoir_volume'] = 0.0

        d['subwell_c_reservoir_volume_unit'] = 'nL'

        try:
            d['subwell_c_seed_volume'] = float(self.subwell_c_seed.value)
        except ValueError:
            d['subwell_c_seed_volume'] = 0.0

        d['subwell_c_seed_volume_unit'] = 'nL'

        try:
            d['subwell_d_protein_volume'] = float(self.subwell_d_protein.value)
        except ValueError:
            d['subwell_d_protein_volume'] = 0.0

        d['subwell_d_protein_volume_unit'] = 'nL'

        try:
            d['subwell_d_reservoir_volume'] = float(self.subwell_d_reservoir.value)
        except ValueError:
            d['subwell_d_reservoir_volume'] = 0.0

        d['subwell_d_reservoir_volume_unit'] = 'nL'

        try:
            d['subwell_d_seed_volume'] = float(self.subwell_d_seed.value)
        except ValueError:
            d['subwell_d_seed_volume'] = 0.0

        d['subwell_d_seed_volume_unit'] = 'nL'

        d['protein_batch_id'] = self.select_protein_batch.value.split(':')[0]
        d['crystallization_method_id'] = self.select_method.value.split(':')[0]
        d['plate_type_id'] = self.select_plate_type.value.split(':')[0]
        d['crystal_screen_id'] = self.select_screen_for_plate.value.split(':')[0]

        barcode =  self.select_barcode.value

        query.save_crystal_plate_to_database(self.logger, self.dal, d, barcode)

#        if self.select_barcode.value in existing_barcodes:
#            self.logger.warning('plate barcode ' + self.select_barcode.value + ' exists in database; updating records...')
#            query = db.update(self.dbObject.crystalplateTable).values(
#                ProteinBatch_ID=self.select_protein_batch.value,
#                Protein_Concentration=_protein_concentration,
#                CrystalScreen_Name=self.select_screen_for_plate.value,
#                Protein_Buffer=self.protein_buffer.value,
#                Temperature=_temperature,
#                Plate_Type=self.select_plate_type.value,
#                Crystallization_Method=self.select_method.value,
#                Reservoir_Volume=_reservoir_volume,
#                Subwell_A_Vol_Protein=_subwell_a_protein,
#                Subwell_A_Vol_Reservoir=_subwell_a_reservoir,
#                Subwell_A_Vol_Seed=_subwell_a_seed,
#                Subwell_C_Vol_Protein=_subwell_c_protein,
#                Subwell_C_Vol_Reservoir=_subwell_c_reservoir,
#                Subwell_C_Vol_Seed=_subwell_c_seed,
#                Subwell_D_Vol_Protein=_subwell_d_protein,
#                Subwell_D_Vol_Reservoir=_subwell_d_reservoir,
#                Subwell_D_Vol_Seed=_subwell_d_seed
#            ).where(self.dbObject.crystalplateTable.columns.CrystalPlate_Barcode == self.select_barcode.value)
#            self.dbObject.connection.execute(query)
#        else:
#            self.logger.info('plate barcode ' + self.select_barcode.value + ' does not exist in database; inserting records...')
#            values_list = [{
#                'CrystalPlate_Barcode': self.select_barcode.value,
#                'ProteinBatch_ID': self.select_protein_batch.value,
#                'Protein_Concentration': _protein_concentration,
#                'CrystalScreen_Name': self.select_screen_for_plate.value,
#                'Protein_Buffer': self.protein_buffer.value,
#                'Temperature': _temperature,
#                'Plate_Type': self.select_plate_type.value,
#                'Crystallization_Method': self.select_method.value,
#                'Reservoir_Volume': _reservoir_volume,
#                'Subwell_A_Vol_Protein': _subwell_a_protein,
#                'Subwell_A_Vol_Reservoir': _subwell_a_reservoir,
#                'Subwell_A_Vol_Seed': _subwell_a_seed,
#                'Subwell_C_Vol_Protein': _subwell_c_protein,
#                'Subwell_C_Vol_Reservoir': _subwell_c_reservoir,
#                'Subwell_C_Vol_Seed': _subwell_c_seed,
#                'Subwell_D_Vol_Protein': _subwell_d_protein,
#                'Subwell_D_Vol_Reservoir': _subwell_d_reservoir,
#                'Subwell_D_Vol_Seed': _subwell_d_seed
#            }]
#            query = db.insert(self.dbObject.crystalplateTable)
#            self.dbObject.connection.execute(query, values_list)

        fs.save_shifter_csv_to_inspect_folder(_subwell_a_protein, _subwell_c_protein, _subwell_d_protein,
                                              self.select_barcode.value, self.select_plate_type.value,
                                              self.settingsObject.workflow_folder)


#    def save_shifter_csv_to_inspect_folder(self, subwell_a, subwell_c, subwell_d, barcode, plate_type):
#        # make backup of file exisits
#        self.logger.info(
#            'writing CSV file for shifter inspection as ' + os.path.join(self.settingsObject.workflow_folder, '1-inspect', barcode + '.csv'))
#        if os.path.isfile(os.path.join(self.settingsObject.workflow_folder, '1-inspect', barcode + '.csv')):
#            self.logger.warning('file exists ' + os.path.join(self.settingsObject.workflow_folder, '1-inspect', barcode + '.csv'))
#            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#            self.logger.info('backing up exisiting file as ' + barcode + '.csv.' + now)
#            move(os.path.join(self.settingsObject.workflow_folder, '1-inspect', barcode + '.csv'),
#                 os.path.join(self.settingsObject.workflow_folder, '1-inspect', 'backup', barcode + '.csv.' + now))
#        csv = ''
#        subwells = []
#        if int(subwell_a) != 0:
#            subwells.append('a')
#        if int(subwell_c) != 0:
#            subwells.append('c')
#        if int(subwell_d) != 0:
#            subwells.append('d')
#        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
#        columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
#        for row in rows:
#            for column in columns:
#                for subwell in subwells:
#                    csv += '{0!s},{1!s},AM,{2!s},{3!s},{4!s},,,,,,,,,\n'.format(plate_type, barcode, row, column, subwell)
#        f = open(os.path.join(self.settingsObject.workflow_folder, '1-inspect', barcode + '.csv'), 'w')
#        f.write(csv)
#        f.close()


    def load_plate_from_db(self, b):
#        self.logger.info('loading information for crystal plate ' + self.select_barcode.value)
#        query = db.select([self.dbObject.crystalplateTable]).where(
#            self.dbObject.crystalplateTable.columns.CrystalPlate_Barcode == self.select_barcode.value)
#        ResultProxy = self.dbObject.connection.execute(query)
#        plate = ResultProxy.fetchall()
#        x = [dict(r) for r in plate][0]
        x = query.load_crystal_plate_from_database(self.dal, self.logger, self.select_barcode.value)
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

#        crystalscreen = str(x['CrystalScreen_Name'])
#        query = db.select([self.dbObject.crystalscreenTable.columns.CrystalScreen_Name.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        existing_crystalscreen = [x[0] for x in ResultProxy.fetchall()]
#        self.select_screen_for_plate.options = existing_crystalscreen
#        self.select_screen_for_plate.value = crystalscreen
