import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
#import sqlalchemy as db
import os
#import re
#from shutil import copyfile
#from datetime import datetime

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import filesystem as fs
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query


class soaked_crystal_tab(object):
    def __init__(self, settingsObject, dal, logger, popup, progress_bar):

        self.settingsObject = settingsObject
        self.dal = dal
        self.logger = logger
        self.popup = popup
        self.progress_bar = progress_bar

        n_rows = 2000

        headerList = [
            'CrystalPlate_Barcode',
            'CrystalPlate_Well',
            'CrystalPlate_Subwell',
            'SoakPlate_Name',
            'SoakPlate_Well',
            'SoakPlate_Subwell',
            'CompoundBatch_ID',
            'Soak_Comment'
                ]

        methods = [
            "shifter (compound to drop)",
            "shifter (crystal to compound)",
            "opentrons workflow (compound to drop)",
            "mosquito transfer (compound to drop)",
            "multichannel pipette transfer (manual; compound to drop)",
            "single pipette transfer (manual; compound to drop)"
        ]

        x = []

        for i in range(1000):
            m = {}
            for j in range(len(headerList)):
                key = headerList[j]
                value = "............"     # cannot be space
                m[key] = value
            x.append(m)

        self.grid_widget = widgets.GridspecLayout(10, 4)

        import_crystal_soak_csv_button = widgets.Button(description='Import CSVs')
        import_crystal_soak_csv_button.on_click(self.import_crystal_soak_csv)
        self.grid_widget[0, 0] = import_crystal_soak_csv_button

        soak_method_button = widgets.Button(description='Method used')
        self.grid_widget[1, 0] = soak_method_button
        self.soak_method_dropdown = widgets.Dropdown()
        self.soak_method_dropdown.options = methods
        self.grid_widget[1, 1] = import_crystal_soak_csv_button

        volume_added_button = widgets.Button(description='Volume added (\u03BCL)')
        self.grid_widget[2,0] = volume_added_button
        self.volume_added = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
        self.grid_widget[2, 1] = self.volume_added

        update_crystal_soak_table_button = widgets.Button(description='Update table')
        update_crystal_soak_table_button.on_click(self.update_crystal_soak_table)
        self.grid_widget[3,0] = update_crystal_soak_table_button

#        need start import button (and show selected file as text)
















    def import_crystal_soak_csv(self, b):
        clear_output()
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        b.files = filedialog.askopenfilename(multiple=True,
                                             initialdir=os.path.join(self.settingsObject.workflow_folder, '2-soak'),
                                             title="select _compound.csv file",
                                             filetypes=[("Text Files", "*.csv")])
        soak_csv = b.files[0]
        if soak_csv.endswith('_compound.csv'):
            soaked_cystal_list, xtbm_list = fs.read_soaked_crystal_csv_from_shifter(self.logger, soak_csv)
            # save xtbm to 3-mount -> 1. does file exist; 2. update existing or insert in new file
            fs.prepare_crystal_mount_csv_for_shifter(self.logger, self.settingsObject.workflow_folder, xtbm_list)
            fs.update_crystal_mount_csv_for_shifter(self.logger, self.settingsObject.workflow_folder, xtbm_list)
            query.save_soaked_crystals_to_database(self.logger, self.dal, soaked_cystal_list, self.progress_bar)
        else:
            self.popup('Wrong file type! Please select a file ending with _compound.csv!')

    def update_crystal_soak_table(self, b):
        self.popup('feature coming soon')

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


