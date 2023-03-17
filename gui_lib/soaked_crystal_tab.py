import ipywidgets as widgets
#from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
#import sqlalchemy as db
import os
#import re
#from shutil import copyfile
#from datetime import datetime
from datetime import datetime

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import soaked_crystal_fs as fs
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query
import soaked_crystal_db as db


class soaked_crystal_tab(object):
    def __init__(self, settingsObject, dal, logger, popup, progress_bar):

        self.settingsObject = settingsObject
        self.dal = dal
        self.logger = logger
        self.popup = popup
        self.progress_bar = progress_bar
        self.soak_csv = None

        methods = [
            "opentrons workflow (compound to drop)",
            "shifter (compound to drop)",
            "shifter (crystal to compound)",
            "mosquito transfer (compound to drop)",
            "multichannel pipette transfer (manual; compound to drop)",
            "single pipette transfer (manual; compound to drop)"
        ]

        self.grid_widget = widgets.GridspecLayout(10, 4)

        self.grid_widget[0, 0] = widgets.Label("CSV file",
                                               layout=widgets.Layout(display="flex", justify_content="center"))
        self.crystal_soak_csv = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[0, 1] = self.crystal_soak_csv
        load_crystal_soak_csv_button = widgets.Button(description='Load')
        load_crystal_soak_csv_button.on_click(self.load_crystal_soak_csv)
        self.grid_widget[0, 2] = load_crystal_soak_csv_button

        self.grid_widget[1, 0] = widgets.Label("Method used",
                                               layout=widgets.Layout(display="flex", justify_content="center"))
        self.soak_method_dropdown = widgets.Dropdown()
        self.soak_method_dropdown.options = methods
        self.grid_widget[1, 1] = self.soak_method_dropdown

        self.grid_widget[2, 0] = widgets.Label("Volume added (\u03BCL)",
                                               layout=widgets.Layout(display="flex", justify_content="center"))
        self.volume_added = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[2, 1] = self.volume_added

        self.grid_widget[3, 0] = widgets.Label("Soak temperature (K)",
                                               layout=widgets.Layout(display="flex", justify_content="center"))
        self.temperature = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[3, 1] = self.temperature

        self.grid_widget[4, 0] = widgets.Label("Soak start time",
                                               layout=widgets.Layout(display="flex", justify_content="center"))
        self.soak_start = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[4, 1] = self.soak_start
        set_current_time_button = widgets.Button(description='current time')
        set_current_time_button.on_click(self.set_current_time)
        self.grid_widget[4, 2] = set_current_time_button

        self.grid_widget[5, 0] = widgets.Label("Comments",
                                               layout=widgets.Layout(display="flex", justify_content="center"))
        self.comment = widgets.Textarea(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[5, 1] = self.comment

        update_csv_db_button = widgets.Button(description='Save Soaked Crystals to DB & CSV',
                                                          layout=widgets.Layout(width="auto"),
                                                          style= {'button_color': 'orange'})
        update_csv_db_button.on_click(self.update_csv_and_db)
        self.grid_widget[6,0:2] = update_csv_db_button


    def set_current_time(self, b):
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.soak_start.value = now

    def load_crystal_soak_csv(self, b):
        clear_output()
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        b.files = filedialog.askopenfilename(multiple=True,
                                             initialdir=os.path.join(self.settingsObject.workflow_folder, '2-soak'),
                                             title="select _compound.csv file",
                                             filetypes=[("Text Files", "*.csv")])
        self.soak_csv = b.files[0]
        if self.soak_csv.endswith('_compound.csv') or self.soak_csv.endswith('_soak.csv'):
            self.crystal_soak_csv.value = self.soak_csv
        else:
            self.popup('Wrong file type! Please select a file ending with _compound.csv or _soak.csv!')

    def update_csv_and_db(self, b):
        if self.soak_csv.endswith('_soak.csv'):
            soaked_cystal_list = fs.read_opentrons_soak_plate_csv_file(self.logger, self.soak_csv)
        else:
            soaked_cystal_list = None
            self.logger.error('only opentrons soaks are supported at the moment')

        if soaked_cystal_list:
            self.logger.info('found {0!s} soaked crystals in plate'.format(len(soaked_cystal_list)))
            self.update_db(soaked_cystal_list)
            self.update_csv(soaked_cystal_list)
        else:
            self.logger.warning('cannot find any soaked crystals in plate')

    def update_db(self, soaked_cystal_list):
        d = {}
        d['soak_plate_name'] = os.path.basename(self.soak_csv).replace('_compound.csv','').replace('_soak.csv','')
        d['soak_method'] = self.soak_method_dropdown.value
        #d['soak_datetime'] = self.soak_start.value
        # now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        # datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        d['soak_datetime'] = datetime.strptime(self.soak_start.value, '%Y/%m/%d %H:%M:%S')
        d['comment'] = self.comment.value

        try:
            d['soak_solution_volume'] = float(self.volume_added.value)
        except ValueError:
            d['soak_solution_volume'] = 0.0
        d['soak_solution_volume_unit'] = 'uL'

        try:
            d['soak_temperature'] = float(self.temperature.value)
        except ValueError:
            d['soak_temperature'] = 0.0
        d['soak_temperature_unit'] = 'K'

        db.save_soaked_crystals_to_database(self.logger, self.dal, soaked_cystal_list, d, self.progress_bar)

    def update_csv(self, soaked_cystal_list):
        fs.save_shifter_csv_file_for_mounting(self.logger,
                                              os.path.join(self.settingsObject.workflow_folder, '3-mount'),
                                              soaked_cystal_list)







#    def update_crystal_mount_csv_file(self, crystal_plate_name, plate_type, row, column, subwell):
#        # check if barcode, row, column, subwell exisit
#        found_well = False
#        for line in open(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv'), encoding='utf-8-sig'):
#            if line.startswith(';'):
#                continue
#            if line.startswith('"'):
#                continue
#            if line.startswith("Column1"):
#                continue
#            plate_name = re.split(r'[,;]+', line)[1]
#            plate_row = re.split(r'[,;]+', line)[3]
#            plate_column = re.split(r'[,;]+', line)[4]
#            plate_subwell = re.split(r'[,;]+', line)[5]
#            if plate_name == crystal_plate_name and plate_row == row and plate_column == str(int(column)) and plate_subwell == subwell:
#                found_well = True
#                self.logger.warning(
#                    'crystal is already flagged for mounting in {0!a}_mount.csv: {1!s}, {2!s}, {3!s}; skipping...'.format(
#                        crystal_plate_name, row, str(int(column)), subwell))
#        if not found_well:
#            self.logger.info(
#                'flagging crystal for mounting in {0!a}_mount.csv: {1!s}, {2!s}, {3!s}; skipping...'.format(
#                    crystal_plate_name, row, column, subwell))
#            f = open(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv'), 'a')
#            f.write('{0!s},{1!s},AM,{2!s},{3!s},{4!s},,,,,,,,,\n'.format(plate_type, crystal_plate_name, row, str(int(column)), subwell))
#            f.close()

#    def prepare_crystal_mount_csv_file(self, crystal_plate_name):
#        if os.path.isfile(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv')):
#            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#            self.logger.warning('creating backup of existing {0!s}_mount.csv file in 3-mount folder'.format(crystal_plate_name))
#            copyfile(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv'),
#                     os.path.join(self.settingsObject.workflow_folder, '3-mount', 'backup', crystal_plate_name + '_mount.csv' + now))
#        else:
#            self.logger.info('creating {0!s}_mount.csv file in 3-mount folder'.format(crystal_plate_name))
#            f = open(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv'), 'w')
#            f.write('')
#            f.close()


#    def update_database(self, soakplate_condition_id, marked_crystal_id, soak_time, comment):
#        soak_id = soakplate_condition_id + '-' + marked_crystal_id
#        query = db.select([self.dbObject.soakedcrystalTable.columns.Soak_ID.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        existing_soak_ids = [x[0] for x in ResultProxy.fetchall()]
#        if soak_id in existing_soak_ids:
#            self.logger.warning('soak ID exists: {0!s}; skipping...'.format(soak_id))
#        else:
#            self.logger.info('inserting soak ID in database: {0!s}'.format(soak_id))
#            values_list = [{
#                'Soak_ID':                  soak_id,
#                'MarkedCrystal_ID':         marked_crystal_id,
#                'SoakPlate_Condition_ID':   soakplate_condition_id,
#                'Soak_Time':                soak_time,
#                'Soak_Comment':             comment
#                    }]
#            query = db.insert(self.dbObject.soakedcrystalTable)
#            self.dbObject.connection.execute(query,values_list)


