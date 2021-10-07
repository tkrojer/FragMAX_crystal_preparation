import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from tkinter import Tk, filedialog
from IPython.display import display,clear_output
import sqlalchemy as db

from shutil import copyfile
from shutil import move
from datetime import datetime
import sqlite3
import csv

import os
import misc


class project_description(object):
    def __init__(self, settingsObject, dbObject, crystalplateObject, logger, lp3_project_folder,
                 db_sql, compoundTable_csv, compoundBatchTable_csv):

        self.settings = settingsObject

        self.dbObject = dbObject

        self.crystalplateObject = crystalplateObject

        self.logger = logger

        self.lp3_project_folder = lp3_project_folder

        self.db_sql = db_sql

        self.compoundTable_csv = compoundTable_csv

        self.compoundBatchTable_csv = compoundBatchTable_csv

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
                                                                    style={'button_color': 'green'},
                                                                    tooltip=misc.select_project_directory_button_tip())
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
        b.folder = filedialog.askdirectory(initialdir=self.lp3_project_folder, title="Select project directory")

        if os.path.isdir(b.folder):
            self.settings.project_folder = b.folder
            self.default_folders()
            self.prepare_db()
            self.project_directory.value = str(self.settings.project_folder)
            self.read_project_from_db()
        else:
            self.logger.error('selected project folder does not exist: ' + str(b.folder))

    def default_folders(self):
        self.settings.db_dir = os.path.join(self.settings.project_folder,'database')
        if os.path.isdir(self.settings.db_dir):
            self.logger.warning('DB folder exists: ' + self.settings.db_dir)
        else:
            self.logger.info('creating DB folder: ' + self.settings.db_dir)
            os.mkdir(self.settings.db_dir)
            os.mkdir(os.path.join(self.settings.db_dir, 'backup'))

        self.settings.crystal_image_folder = os.path.join(self.settings.project_folder,'crystal_images')
        if os.path.isdir(self.settings.crystal_image_folder):
            self.logger.warning('crystal image folder exists: ' + self.settings.crystal_image_folder)
        else:
            self.logger.info('creating crystal image folder: ' + self.settings.crystal_image_folder)
            os.mkdir(self.settings.crystal_image_folder)

        self.settings.crystal_screen_folder = os.path.join(self.settings.project_folder, 'crystal_screen')
        if os.path.isdir(self.settings.crystal_screen_folder):
            self.logger.warning('crystal screen folder exists: ' + self.settings.crystal_screen_folder)
        else:
            self.logger.info('creating screen image folder: ' + self.settings.crystal_screen_folder)
            os.mkdir(self.settings.crystal_screen_folder)

        self.settings.workflow_folder = os.path.join(self.settings.project_folder, 'workflow')
        if os.path.isdir(self.settings.workflow_folder):
            self.logger.warning('workflow folder exists: ' + self.settings.workflow_folder)
        else:
            self.logger.info('creating workflow folder: ' + self.settings.workflow_folder)
            os.mkdir(self.settings.workflow_folder)

        workflow_inspect_folder = os.path.join(self.settings.project_folder, 'workflow', '1-inspect')
        if os.path.isdir(workflow_inspect_folder):
            self.logger.warning('workflow/1-inspect folder exists: ' + workflow_inspect_folder)
        else:
            self.logger.info('creating workflow/1-inspect folder: ' + workflow_inspect_folder)
            os.mkdir(workflow_inspect_folder)
            os.mkdir(os.path.join(workflow_inspect_folder, 'backup'))

        workflow_soak_folder = os.path.join(self.settings.project_folder, 'workflow', '2-soak')
        if os.path.isdir(workflow_soak_folder):
            self.logger.warning('workflow/2-soak folder exists: ' + workflow_soak_folder)
        else:
            self.logger.info('creating workflow/2-soak folder: ' + workflow_soak_folder)
            os.mkdir(workflow_soak_folder)
            os.mkdir(os.path.join(workflow_soak_folder, 'backup'))

        workflow_mount_folder = os.path.join(self.settings.project_folder, 'workflow', '3-mount')
        if os.path.isdir(workflow_mount_folder):
            self.logger.warning('workflow/3-mount folder exists: ' + workflow_mount_folder)
        else:
            self.logger.info('creating workflow/3-mount folder: ' + workflow_mount_folder)
            os.mkdir(workflow_mount_folder)
            os.mkdir(os.path.join(workflow_mount_folder, 'backup'))

        workflow_mount_manual_folder = os.path.join(self.settings.project_folder, 'workflow', '4-mount-manual')
        if os.path.isdir(workflow_mount_manual_folder):
            self.logger.warning('workflow/4-mount-manual folder exists: ' + workflow_mount_manual_folder)
        else:
            self.logger.info('creating workflow/4-mount-manual folder: ' + workflow_mount_manual_folder)
            os.mkdir(workflow_mount_manual_folder)
            os.mkdir(os.path.join(workflow_mount_manual_folder, 'backup'))

        workflow_exi_folder = os.path.join(self.settings.project_folder, 'workflow', '5-exi')
        if os.path.isdir(workflow_exi_folder):
            self.logger.warning('workflow/5-exi folder exists: ' + workflow_exi_folder)
        else:
            self.logger.info('creating workflow/5-exi folder: ' + workflow_exi_folder)
            os.mkdir(workflow_exi_folder)
            os.mkdir(os.path.join(workflow_exi_folder, 'backup'))

        workflow_fragmaxapp_folder = os.path.join(self.settings.project_folder, 'workflow', '6-fragmaxapp')
        if os.path.isdir(workflow_fragmaxapp_folder):
            self.logger.warning('workflow/6-fragmaxapp folder exists: ' + workflow_fragmaxapp_folder)
        else:
            self.logger.info('creating workflow/6-fragmaxapp folder: ' + workflow_fragmaxapp_folder)
            os.mkdir(workflow_fragmaxapp_folder)
            os.mkdir(os.path.join(workflow_fragmaxapp_folder, 'backup'))

        self.settings.eln_folder = os.path.join(self.settings.project_folder,'eln')
        if os.path.isdir(self.settings.eln_folder):
            self.logger.warning('eln folder exists: ' + self.settings.eln_folder)
        else:
            self.logger.info('eln image folder: ' + self.settings.eln_folder)
            os.mkdir(self.settings.eln_folder)


    def init_db(self):
        self.logger.info('initializing DB...')
        self.dbObject.engine = db.create_engine('sqlite:///' + self.settings.db_file)
        self.dbObject.connection = self.dbObject.engine.connect()
        metadata = db.MetaData()

        self.dbObject.projectTable = db.Table('Project', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.crystalscreenTable = db.Table('CrystalScreen', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.proteinTable = db.Table('Protein', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.proteinBatchTable = db.Table('ProteinBatch', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.crystal_plate_typeTable = db.Table('CrystalPlateType', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.crystallizationMethodTable = db.Table('CrystallizationMethod', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.crystalplateTable = db.Table('CrystalPlate', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.markedcrystalTable = db.Table('MarkedCrystals', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.soakplateTable = db.Table('SoakPlate', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.compoundbatchTable = db.Table('CompoundBatchTable', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.compoundTable = db.Table('CompoundTable', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.soakedcrystalTable = db.Table('SoakedCrystals', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.mountedcrystalTable = db.Table('MountedCrystals', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.dbObject.diaryTable = db.Table('Diary', metadata, autoload=True, autoload_with=self.dbObject.engine)

        self.logger.info('defining joined tables...')

        self.dbObject.joined_tables = self.dbObject.mountedcrystalTable.join(
            self.dbObject.soakedcrystalTable, self.dbObject.mountedcrystalTable.columns.SoakPlate_Condition_ID ==
                                              self.dbObject.soakedcrystalTable.columns.SoakPlate_Condition_ID, isouter=True).join(
            self.dbObject.soakplateTable, self.dbObject.soakedcrystalTable.columns.SoakPlate_Condition_ID ==
                                          self.dbObject.soakplateTable.columns.SoakPlate_Condition_ID, isouter=True).join(
            self.dbObject.compoundbatchTable, self.dbObject.soakplateTable.columns.CompoundBatch_ID ==
                                              self.dbObject.compoundbatchTable.columns.CompoundBatch_ID, isouter=True).join(
            self.dbObject.compoundTable, self.dbObject.compoundbatchTable.columns.Compound_ID ==
                                              self.dbObject.compoundTable.columns.Compound_ID, isouter=True).join(
            self.dbObject.markedcrystalTable, self.dbObject.mountedcrystalTable.columns.MarkedCrystal_ID ==
                                         self.dbObject.markedcrystalTable.columns.MarkedCrystal_ID, isouter=True).join(
            self.dbObject.crystalscreenTable, self.dbObject.markedcrystalTable.columns.CrystalScreen_ID ==
                                              self.dbObject.crystalscreenTable.columns.CrystalScreen_ID, isouter=True).join(
            self.dbObject.crystalplateTable, self.dbObject.markedcrystalTable.columns.CrystalPlate_Barcode ==
                                              self.dbObject.crystalplateTable.columns.CrystalPlate_Barcode, isouter=True)

        self.logger.info('finished initializing DB')


    def prepare_db(self):
        self.settings.db_file = os.path.join(self.settings.db_dir, 'fragmax.sqlite')
        self.logger.info("checking if database exists in {0!s}".format(self.settings.db_file))
        if os.path.isfile(str(self.settings.db_file)):
            self.backup_db()
            self.logger.info("found database file")
            self.init_db()
        else:
            self.logger.warning("cannot find database file")
            self.create_new_db()

    def create_new_db(self):
        self.logger.info('creating new database file in {0!s}'.format(self.settings.db_file))
        connect = sqlite3.connect(self.settings.db_file)
        cursor = connect.cursor()
        sql_file = open(self.db_sql)
        self.logger.info('--> ' + self.db_sql)
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
        connect.commit()
        self.populate_compoundTable()
        self.populate_compoundbatchTable()
        self.init_db()

    def populate_compoundbatchTable(self):
        self.logger.info('populating compoundBatchTable with {0!s}'.format(self.compoundBatchTable_csv))
        connect = sqlite3.connect(self.settings.db_file)
        cursor = connect.cursor()
        with open(self.compoundBatchTable_csv) as f:
            data = csv.DictReader(f)
            cols = data.fieldnames
            sql = 'insert into "CompoundBatchTable" values ( {vals} )'.format(
                vals=','.join('?' for col in cols))
            cursor.executemany(sql, (list(map(row.get, cols)) for row in data))
        connect.commit()
#        csv_file = open(self.compoundBatchTable_csv)
#        rows = csv.reader(csv_file)
#        next(rows, None)  # skip the headers
#        cursor.executemany("INSERT INTO CompoundBatchTable VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
#        connect.commit()

    def populate_compoundTable(self):
        self.logger.info('populating compoundTable with {0!s}'.format(self.compoundTable_csv))
        connect = sqlite3.connect(self.settings.db_file)
        cursor = connect.cursor()
        with open(self.compoundTable_csv) as f:
            data = csv.DictReader(f)
            cols = data.fieldnames
            sql = 'insert into "CompoundTable" values ( {vals} )'.format(
                vals=','.join('?' for col in cols))
            cursor.executemany(sql, (list(map(row.get, cols)) for row in data))
        connect.commit()


    def backup_db(self):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.logger.info('creating backup current DB file: ' + os.path.join(self.settings.db_dir,
                                                                            'backup', 'fragmax.sqlite.' + now))
        copyfile(self.settings.db_file, os.path.join(self.settings.db_dir, 'backup', 'fragmax.sqlite.' + now))


    def read_project(self, b):
        self.read_project_from_db()


    def read_project_from_db(self):
        query = db.select([self.dbObject.projectTable])
        ResultProxy = self.dbObject.connection.execute(query)
        results = ResultProxy.fetchall()
        try:
            x = [dict(r) for r in results][0]
            self.project_name.value = str(x['Project_Name'])
            self.proposal_id.value = str(x['Proposal_ID'])
        except IndexError:
            self.logger.warning('no project name and proposal ID registered in DB')

        query = db.select([self.dbObject.proteinTable])
        ResultProxy = self.dbObject.connection.execute(query)
        results = ResultProxy.fetchall()
        try:
            x = [dict(r) for r in results][0]
            self.protein_name.value = str(x['Protein_Name'])
            self.protein_acronym.value = str(x['Protein_Acronym'])
        except IndexError:
            self.logger.warning('no protein name and protein acronym registered in DB')

        self.update_crystal_plate_widgets()

    def save_project(self, b):
        query = db.select([self.dbObject.projectTable.columns.Proposal_ID.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_project_id = [x[0] for x in ResultProxy.fetchall()]

        self.logger.info('existing project_id: ' + str(existing_project_id))

        if existing_project_id == []:
            self.logger.info(
                'adding project information: {0!s}, {1!s}'.format(self.project_name.value, self.proposal_id.value.replace(' ', '')))
            values_list = [{
                'Project_Name': self.project_name.value,
                'Proposal_ID': self.proposal_id.value.replace(' ', '')
            }]
            query = db.insert(self.dbObject.projectTable)
            self.dbObject.connection.execute(query, values_list)
        else:
            self.logger.info(
                'updating project information: {0!s}, {1!s}'.format(self.project_name.value, self.proposal_id.value.replace(' ', '')))
            query = db.update(self.dbObject.projectTable).values(
                Project_Name=self.project_name.value,
                Proposal_ID=self.proposal_id.value.replace(' ', '')).where(
                self.dbObject.projectTable.columns.Proposal_ID == existing_project_id[0])
            self.dbObject.connection.execute(query)

        query = db.select([self.dbObject.proteinTable.columns.Protein_Acronym.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_protein_acronym = [x[0] for x in ResultProxy.fetchall()]

        if existing_protein_acronym == []:
            values_list = [{
                'Protein_Name': self.protein_name.value,
                'Protein_Acronym': self.protein_acronym.value.replace(' ', '')
            }]
            query = db.insert(self.dbObject.proteinTable)
            self.dbObject.connection.execute(query, values_list)
        else:
            query = db.update(self.dbObject.proteinTable).values(
                Protein_Name=self.protein_name.value,
                Protein_Acronym=self.protein_acronym.value.replace(' ', '')).where(
                self.dbObject.proteinTable.columns.Protein_Acronym == existing_protein_acronym[0])
            self.dbObject.connection.execute(query)

        self.update_crystal_plate_widgets()


    def update_crystal_plate_widgets(self):
        query = db.select([self.dbObject.proteinBatchTable.columns.ProteinBatch_ID.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_protein_batches = [x[0] for x in ResultProxy.fetchall()]
        self.logger.info('found the following protein batches in database: ' + str(existing_protein_batches))
        self.crystalplateObject.select_protein_batch.options = existing_protein_batches

        query = db.select([self.dbObject.crystal_plate_typeTable.columns.Plate_Name.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_plate_types = [x[0] for x in ResultProxy.fetchall()]
        self.logger.info('found the following crystal plate types in database: ' + str(existing_plate_types))
        self.crystalplateObject.select_plate_type.options = existing_plate_types

        query = db.select([self.dbObject.crystallizationMethodTable.columns.Method.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_methods = [x[0] for x in ResultProxy.fetchall()]
        self.logger.info('found the following crystallization methods in database: ' + str(existing_methods))
        self.crystalplateObject.select_method.options = existing_methods
