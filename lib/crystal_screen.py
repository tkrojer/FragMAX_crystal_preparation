import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
import misc
import pandas as pd
import qgrid
from shutil import copyfile
from tkinter import Tk, filedialog
import ntpath
import sqlalchemy as db
import os


class crystal_screen(object):
    def __init__(self, settingsObject, dbObject, logger, crystal_plate_template):

        self.settings = settingsObject

        self.dbObject = dbObject

        self.logger = logger

        self.crystal_plate_template = crystal_plate_template

        self.grid_widget = widgets.GridspecLayout(3, 4)

        self.grid_widget[0, 0] = Label("Enter New Screen Name", layout=Layout(display="flex", justify_content="center"))

        self.screen_name = widgets.Text(value='', layout=widgets.Layout(height="auto", width="auto"))
        self.grid_widget[0, 1] = self.screen_name
        self.add_screen_button = widgets.Button(description='Add', tooltip=misc.add_screen_button_tip())
        self.add_screen_button.on_click(self.add_screen)
        self.grid_widget[0, 2] = self.add_screen_button
        self.grid_widget[1, 0] = Label("Select Screen", layout=Layout(display="flex", justify_content="center"))
        self.select_screen = widgets.Dropdown()
        self.grid_widget[1, 1] = self.select_screen

        self.refresh_screen_button = widgets.Button(description='Refresh Screen List',
                                               tooltip=misc.refresh_screen_button_tip())
        self.refresh_screen_button.on_click(self.refresh_screen_dropdown)
        self.grid_widget[1, 2] = self.refresh_screen_button

        self.load_selected_screen_button = widgets.Button(description="Load Screen from DB",
                                                     layout=widgets.Layout(height="auto", width="auto"),
                                                     tooltip=misc.load_selected_screen_button_tip())
        self.load_selected_screen_button.on_click(self.load_screen_from_db)
        self.grid_widget[2, 0] = self.load_selected_screen_button

        self.save_screen_csv_button = widgets.Button(description="Save CSV template",
                                                layout=widgets.Layout(height="auto", width="auto"),
                                                tooltip=misc.save_screen_csv_button_tip(str(self.settings.crystal_screen_folder),
                                                                                        str(self.select_screen.value)))
        self.save_screen_csv_button.on_click(self.save_screen_csv)
        self.grid_widget[2, 1] = self.save_screen_csv_button

        self.upload_screen_csv_button = widgets.Button(description="Upload CSV file",
                                                  layout=widgets.Layout(height="auto", width="auto"))
        self.upload_screen_csv_button.on_click(self.upload_screen_csv)
        self.grid_widget[2, 2] = self.upload_screen_csv_button

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

        self.crystal_screen_progress = IntProgress(min=0, max=95)


    def add_screen(self, b):
        self.add_screen_to_dropdown()


    def add_screen_to_dropdown(self):
        l = []
        for opt in self.select_screen.options: l.append(opt)
        if self.screen_name.value not in l:
            self.logger.info('adding ' + self.screen_name.value + ' to screen dropdown')
            l.append(self.screen_name.value)
        else:
            self.logger.warning(self.screen_name.value + ' exists in screen dropdown')
        self.select_screen.options = l

    def refresh_screen_dropdown(self, b):
        query = db.select([self.dbObject.crystalscreenTable.columns.CrystalScreen_Name.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_crystalscreens = [x[0] for x in ResultProxy.fetchall()]
        self.select_screen.options = existing_crystalscreens
        self.logger.info('updating screen selection dropdown: ' + str(existing_crystalscreens))

    def load_screen_from_db(self, b):
        query = db.select([self.dbObject.crystalscreenTable.columns.CrystalScreen_Name.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_crystalscreens = [x[0] for x in ResultProxy.fetchall()]
        if self.select_screen.value in existing_crystalscreens:
            self.logger.info('screen ' + self.select_screen.value + ' exists in database')
            query = db.select([self.dbObject.crystalscreenTable.columns.CrystalScreen_Well,
                              self.dbObject.crystalscreenTable.columns.CrystalScreen_Condition]).where(
                              self.dbObject.crystalscreenTable.columns.CrystalScreen_Name == self.select_screen.value)
#            ResultProxy = connection.execute(query)
#            result = ResultProxy.fetchall()
            self.logger.info('loading information for screen {0!s} from database'.format(self.select_screen.value))
            df = pd.read_sql_query(query, self.dbObject.engine)
            self.screen_sheet.df = df
        else:
            self.logger.warning('screen {0!s} does not exist in database; skipping...'.format(self.select_screen.value))

    def save_screen_csv(self, b):
        CrystalScreen_Name = self.select_screen.value.replace(' ','')
        self.logger.warning('removing whitespaces from crystal screen name: ' + CrystalScreen_Name)
        self.logger.info('trying to copy empty crystal screen CSV template with name ' +
                         CrystalScreen_Name + ' to ' + self.settings.crystal_screen_folder)
        if os.path.isfile(os.path.join(self.settings.crystal_screen_folder, CrystalScreen_Name + '.csv')):
            self.logger.error('file exists in ' + os.path.join(self.settings.crystal_screen_folder, CrystalScreen_Name + '.csv'))
        else:
            self.logger.info('creating new template ' + os.path.join(self.settings.crystal_screen_folder, CrystalScreen_Name + '.csv'))
            copyfile(self.crystal_plate_template, os.path.join(self.settings.crystal_screen_folder, CrystalScreen_Name + '.csv'))

    def upload_screen_csv(self, b):
        clear_output()
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        b.files = filedialog.askopenfilename(multiple=True)
        if os.path.isfile(b.files[0]):
            self.logger.info('loading ' + b.files[0])
            self.screen_name.value = ntpath.basename(b.files[0]).split('.')[0]
            self.add_screen_to_dropdown()
            df = pd.read_csv(b.files[0], sep=';')
            self.screen_sheet.df = df
        else:
            self.logger.error('cannot read file ' + b.files[0])


    def save_dragonfly_to_csv(self, dragonflyFile):
        csv = 'CrystalScreen_Well,CrystalScreen_Condition\n'
        new_condition = False
        for line in open(dragonflyFile):
            if new_condition and line.replace('\n', '') == '':
                csv += well + ',' + condition[:-3] + '\n'
                new_condition = False
            if new_condition:
                condition += line.replace('\n', '').replace(',', '.') + ' - '
            if line.endswith(':\n') and not 'Components' in line:
                well = line.replace(':\n', '')
                if len(well) == 2:
                    well = well[0] + '0' + well[1]
                new_condition = True
                condition = ''
        self.logger.info('saving dragonfly txt file as csv: ' + dragonflyFile.replace('.txt', '.csv'))
        f = open(dragonflyFile.replace('.txt', '.csv'), 'w')
        f.write(csv)
        f.close()


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
        CrystalScreen_Name = self.select_screen.value.replace(' ','')
        self.logger.info('saving ' + CrystalScreen_Name + ' crystal screen to database')

        query = db.select([self.dbObject.crystalscreenTable.columns.CrystalScreen_Name.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_crystalscreens = [x[0] for x in ResultProxy.fetchall()]

        for index, row in df.iterrows():
            self.crystal_screen_progress.value = index
            condition = df.at[index,'CrystalScreen_Condition']
            well = df.at[index,'CrystalScreen_Well']
            self.logger.info("-- {0!s} {1!s}".format(well, condition))
            screen_id = CrystalScreen_Name + '-' + well
            if CrystalScreen_Name in existing_crystalscreens:
                self.logger.warning('crystal screen exists in database; updating records: {0!s} - {1!s}'.format(well, condition))
                query = db.update(self.dbObject.crystalscreenTable).values(
                    CrystalScreen_Condition = condition).where(
                    self.dbObject.crystalscreenTable.columns.CrystalScreen_ID == screen_id)
                self.dbObject.connection.execute(query)
            else:
                self.logger.info('crystal screen does not exist in database; inserting records: {0!s} - {1!s}'.format(well, condition))
                values_list = [{
                    'CrystalScreen_Condition': condition,
                    'CrystalScreen_Well':      well,
                    'CrystalScreen_Name':      CrystalScreen_Name,
                    'CrystalScreen_ID':        screen_id
                }]
                query = db.insert(self.dbObject.crystalscreenTable)
                self.dbObject.connection.execute(query,values_list)
            crystal_screen_progress.value = 0
