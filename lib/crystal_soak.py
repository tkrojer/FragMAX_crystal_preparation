import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
import sqlalchemy as db
import os
import re
from shutil import copyfile
from datetime import datetime

class crystal_soak(object):
    def __init__(self, settingsObject, dbObject, logger):

        self.settingsObject = settingsObject

        self.dbObject = dbObject

        self.logger = logger

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
        self.grid_widget[0,3] = import_crystal_soak_csv_button

        update_crystal_soak_table_button = widgets.Button(description='Update table')
        update_crystal_soak_table_button.on_click(self.update_crystal_soak_table)
        self.grid_widget[1,3] = update_crystal_soak_table_button


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
            self.logger.info('reading {0!s} file...'.format(soak_csv))
            crystal_plate_list = []
            for line in open(soak_csv, encoding='utf-8-sig'):
                if line.startswith(';'):
                    continue
                elif line.startswith('PlateType'):
                    continue
                # crystal_id is irrelevant, but if field is blank then nothing was transferred
                crystal_id = re.split(r'[,;]+', line)[7].replace(' ','')
                if crystal_id == '':
                    continue
                try:
                    plate_type = re.split(r'[,;]+', line)[0]
                    compound_plate_name = re.split(r'[,;]+', line)[1]
                    compound_plate_row = re.split(r'[,;]+', line)[3]
                    compound_plate_column = '0' * (2 - len(re.split(r'[,;]+', line)[4])) + re.split(r'[,;]+', line)[4]
                    compound_plate_subwell = re.split(r'[,;]+', line)[5]
                    soak_time = re.split(r'[,;]+', line)[9]
                    comment = re.split(r'[,;]+', line)[6]
                    crystal_plate_name = re.split(r'[,;]+', line)[11].replace('Right: ','').replace('Left: ','')
                    crystal_plate_row = re.split(r'[,;]+', line)[12][0]
                    crystal_plate_column = ''
                    if len(re.split(r'[,;]+', line)[12]) == 3:
                        crystal_plate_column = '0' + re.split(r'[,;]+', line)[12][1]
                    elif len(re.split(r'[,;]+', line)[12]) == 4:
                        crystal_plate_column = re.split(r'[,;]+', line)[12][1:3]
                    crystal_plate_subwell = re.split(r'[,;]+', line)[12][-1]

                    # save each row to csv file in 3-mount folder?
                    if crystal_plate_name not in crystal_plate_list:
                        crystal_plate_list.append(crystal_plate_name)
                        self.prepare_crystal_mount_csv_file(crystal_plate_name)
                    self.update_crystal_mount_csv_file(crystal_plate_name, plate_type, crystal_plate_row, crystal_plate_column, crystal_plate_subwell)

#                    soakplate_condition_id = compound_plate_name + '-' + compound_plate_row + \
#                                             compound_plate_column + compound_plate_subwell

                    # subwell is omitted for the time being since only one subwell is used for soaking
                    soakplate_condition_id = compound_plate_name + '-' + compound_plate_row + \
                                             compound_plate_column

                    marked_crystal_id = crystal_plate_name + '-' + crystal_plate_row + \
                                        crystal_plate_column + crystal_plate_subwell

                    self.update_database(soakplate_condition_id, marked_crystal_id, soak_time, comment)
                except IndexError:
                    continue

        else:
            self.logger.error('Wrong file type! Please select a file ending with _compound.csv!')


    def update_crystal_mount_csv_file(self, crystal_plate_name, plate_type, row, column, subwell):
        # check if barcode, row, column, subwell exisit
        found_well = False
        for line in open(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv'), encoding='utf-8-sig'):
            plate_name = re.split(r'[,;]+', line)[1]
            plate_row = re.split(r'[,;]+', line)[3]
            plate_column = re.split(r'[,;]+', line)[4]
            plate_subwell = re.split(r'[,;]+', line)[5]
            if plate_name == crystal_plate_name and plate_row == row and plate_column == str(int(column)) and plate_subwell == subwell:
                found_well = True
                self.logger.warning(
                    'crystal is already flagged for mounting in {0!a}_mount.csv: {1!s}, {2!s}, {3!s}; skipping...'.format(
                        crystal_plate_name, row, str(int(column)), subwell))
        if not found_well:
            self.logger.info(
                'flagging crystal for mounting in {0!a}_mount.csv: {1!s}, {2!s}, {3!s}; skipping...'.format(
                    crystal_plate_name, row, column, subwell))
            f = open(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv'), 'a')
            f.write('{0!s},{1!s},AM,{2!s},{3!s},{4!s},,,,,,,,,\n'.format(plate_type, crystal_plate_name, row, str(int(column)), subwell))
            f.close()

    def prepare_crystal_mount_csv_file(self, crystal_plate_name):
        if os.path.isfile(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv')):
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.logger.warning('creating backup of existing {0!s}_mount.csv file in 3-mount folder'.format(crystal_plate_name))
            copyfile(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv'),
                     os.path.join(self.settingsObject.workflow_folder, '3-mount', 'backup', crystal_plate_name + '_mount.csv' + now))
        else:
            self.logger.info('creating {0!s}_mount.csv file in 3-mount folder'.format(crystal_plate_name))
            f = open(os.path.join(self.settingsObject.workflow_folder, '3-mount', crystal_plate_name + '_mount.csv'), 'w')
            f.write('')
            f.close()


    def update_database(self, soakplate_condition_id, marked_crystal_id, soak_time, comment):
        soak_id = soakplate_condition_id + '-' + marked_crystal_id
        query = db.select([self.dbObject.soakedcrystalTable.columns.Soak_ID.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_soak_ids = [x[0] for x in ResultProxy.fetchall()]
        if soak_id in existing_soak_ids:
            self.logger.warning('soak ID exists: {0!s}; skipping...'.format(soak_id))
        else:
            self.logger.info('inserting soak ID in database: {0!s}; skipping...'.format(soak_id))
            values_list = [{
                'Soak_ID':                  soak_id,
                'MarkedCrystal_ID':         marked_crystal_id,
                'SoakPlate_Condition_ID':   soakplate_condition_id,
                'Soak_Time':                soak_time,
                'Soak_Comment':             comment
                    }]
            query = db.insert(self.dbObject.soakedcrystalTable)
            self.dbObject.connection.execute(query,values_list)


    def update_crystal_soak_table(self, b):
        self.logger.error('implementation pending!!!!!!!!!!!!!!')
