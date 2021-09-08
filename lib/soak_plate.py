import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
import sqlalchemy as db
import pandas as pd
from datetime import datetime
import misc


class soak_plate(object):
    def __init__(self, settingsObject, dbObject, logger):

        self.settingsObject = settingsObject

        self.dbObject = dbObject

        self.logger = logger
        
        self.grid_widget = widgets.GridspecLayout(10, 4)

        self.grid_widget[0,0] = widgets.Button(description="Enter New Soak Plate Name", 
                           layout=widgets.Layout(height="auto", width="auto"), style= {'button_color':'white'})
        self.soakplate_name = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[0,1] = self.soakplate_name
        add_soakplate_name_button = widgets.Button(description='Add')
        add_soakplate_name_button.on_click(self.add_soakplate)
        self.grid_widget[0,2] = add_soakplate_name_button

        self.grid_widget[1,0] = widgets.Button(description="Select Soak Plate", 
                           layout=widgets.Layout(height="auto", width="auto"), style= {'button_color':'white'})
        self.select_soakplate = widgets.Dropdown()
        self.grid_widget[1,1] = self.select_soakplate
        refresh_soakplate_button = widgets.Button(description='Refresh Soak Plate List')
        refresh_soakplate_button.on_click(self.refresh_soakplate)
        self.grid_widget[1,2] = refresh_soakplate_button

        self.grid_widget[2,0] = widgets.Button(description="Select Library Plate", 
                           layout=widgets.Layout(height="auto", width="auto"), style= {'button_color':'white'})
        self.select_library_plate = widgets.Dropdown()
        self.grid_widget[2,1] = self.select_library_plate
        refresh_library_plate_button = widgets.Button(description='Refresh Library Plate List')
        refresh_library_plate_button.on_click(self.refresh_libraryplate)
        self.grid_widget[2,2] = refresh_library_plate_button

        self.grid_widget[3,0] = widgets.Button(description="Reservoir Condition", 
                           layout=widgets.Layout(height="auto", width="auto"), style= {'button_color':'white'})
        self.soakplate_reservoir = widgets.Text(value='', layout=widgets.Layout(height="auto", width="200"))
        self.grid_widget[3,1:] = self.soakplate_reservoir

        self.grid_widget[4,0] = widgets.Button(description="Reservoir Volume (\u03BCL)", 
                           layout=widgets.Layout(height="auto", width="auto"), style= {'button_color':'white'})
        self.soakplate_reservoir_volume = widgets.Text(value='', layout=widgets.Layout(height="auto", width="200"))
        self.grid_widget[4,1:] = self.soakplate_reservoir_volume

        self.grid_widget[5,0] = widgets.Button(description="Compound Volume (\u03BCL)", 
                           layout=widgets.Layout(height="auto", width="auto"), style= {'button_color':'white'})
        self.soakplate_compound_volume = widgets.Text(value='', layout=widgets.Layout(height="auto", width="200"))
        self.grid_widget[5,1] = self.soakplate_compound_volume

        save_soakplate_button = widgets.Button(description='Save Soak Plate to DB',  style= {'button_color':'gray'})
        save_soakplate_button.on_click(self.save_soakplate_to_db)
        self.grid_widget[6,0:] = save_soakplate_button


    def add_soakplate(self, b):
        l = []
        for opt in self.select_soakplate.options: l.append(opt)
        if self.soakplate_name.value not in l:
            self.logger.info('adding ' + self.soakplate_name.value + ' to soakplate dropdown')
            l.append(self.soakplate_name.value)
        else:
            self.logger.warning(self.soakplate_name.value + ' exists in soakplate dropdown')
        self.select_soakplate.options = l


    def refresh_soakplate(self, b):
        query = db.select([self.dbObject.soakplateTable.columns.SoakPlate_Name.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_soakplates = [x[0] for x in ResultProxy.fetchall()]
        self.select_soakplate.options = existing_soakplates
        self.logger.info('updating soakplate dropdown: ' + str(existing_soakplates))


    def refresh_libraryplate(self, b):
        query = db.select([self.dbObject.compoundbatchTable.columns.CompoundPlate_Name.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_compoundplates = [x[0] for x in ResultProxy.fetchall()]
        self.select_library_plate.options = existing_compoundplates
        self.logger.info('updating Library plate selection dropdown: ' + str(existing_compoundplates))


    def save_soakplate_to_db(self, b):
        self.logger.info('saving soakplate information for ' + self.select_soakplate.value + ' to database')
        query = db.select([self.dbObject.soakplateTable.columns.SoakPlate_Name.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_soakplates = [x[0] for x in ResultProxy.fetchall()]

        df_template = pd.read_csv(crystal_plate_template)
        for index, row in df_template.iterrows():
            well = df_template.at[index, 'CrystalScreen_Well']

        query = db.select([self.dbObject.compoundbatchTable.columns.CompoundPlate_Well,
                            compoundbatchTable.columns.CompoundBatch_ID]).where(
                            compoundbatchTable.columns.CompoundPlate_Name == select_library_plate.value)
        ResultProxy = self.dbObject.connection.execute(query)
        results = ResultProxy.fetchall()

        try:
            _soakplate_reservoir_volume = float(self.soakplate_reservoir_volume.value)
        except ValueError:
            _soakplate_reservoir_volume = 0.0

        try:
            _soakplate_compound_volume = float(self.soakplate_compound_volume.value)
        except ValueError:
            _soakplate_compound_volume = 0.0

        soakRows = []
        for r in results:
            well = r[0]
            column = well[0]
            row = well[1:3]
            cpd = r[1]
            soakplate_condition_id = self.select_soakplate.value + '-' + well

            if select_soakplate.value in existing_soakplates:
                self.logger.warning('soakplate ' + self.select_soakplate.value + ' exists in database; updating records...')
                query = db.update(self.dbObject.soakplateTable).values(
                    SoakPlate_Name=self.select_soakplate.value,
                    SoakPlate_Well=well,
                    SoakPlate_Subwell='a',
                    CompoundBatch_ID=cpd,
                    CompoundPlate_Name=self.select_library_plate.value,
                    CrystalBuffer=self.soakplate_reservoir.value,
                    CrystalBuffer_Vol=_soakplate_reservoir_volume,
                    Compound_Vol=_soakplate_compound_volume
                ).where(self.dbObject.soakplateTable.columns.SoakPlate_Condition_ID == soakplate_condition_id)
                self.dbObject.connection.execute(query)
            else:
                self.logger.info('plate barcode ' + self.select_soakplate.value + ' does not exist in database; inserting records...')
                values_list = [{
                    'SoakPlate_Condition_ID': soakplate_condition_id,
                    'SoakPlate_Name': self.select_soakplate.value,
                    'SoakPlate_Well': well,
                    'SoakPlate_Subwell': 'a',
                    'CompoundBatch_ID': cpd,
                    'CompoundPlate_Name': self.select_library_plate.value,
                    'CrystalBuffer': self.soakplate_reservoir.value,
                    'CrystalBuffer_Vol': _soakplate_reservoir_volume,
                    'Compound_Vol': _soakplate_compound_volume
                }]
                query = db.insert(self.dbObject.soakplateTable)
                self.dbObject.connection.execute(query, values_list)

            soakRowDict = {
                'PlateType': 'SwissCI-MRC-3d',
                'PlateID': self.select_soakplate.value,
                'LocationShifter': 'AM',
                'PlateColumn': column,
                'PlateRow': row,
                'PositionSubWell': 'a',
                'ExternalComment': cpd
            }
            soakRows.append(soakRowDict)

        self.save_soakplate_csv_files(soakRows, select_soakplate.value)


    def save_soakplate_csv_files(self, soakRows, soakPlate):
        if os.path.isfile(os.path.join(self.settingsObject.workflow_folder, '2-soak', soakPlate + '_compound.csv')):
            self.logger.warning('soakplate CSV file exists: ' + os.path.join(self.settingsObject.workflow_folder, '2-soak', soakPlate + '_compound.csv'))
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.logger.info('moving exisiting soakplate CSV file to backup folder as: ' + soakPlate + '_compound.csv.' + now)
            move(os.path.join(self.settingsObject.workflow_folder, '2-soak', soakPlate + '_compound.csv'),
                 os.path.join(self.settingsObject.workflow_folder, '2-soak', 'backup', soakPlate + '_compound.csv.' + now))

        fieldnames = misc.shifter_csv_header()
        with open(os.path.join(self.settingsObject.workflow_folder, '2-soak', soakPlate + '_compound.csv'), 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(soakRows)
