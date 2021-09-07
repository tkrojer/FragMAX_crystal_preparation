import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
import os
import re

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
            'Soak_Date',
            'Soak_Behaviour'
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


#    def import_soaked_crystals(self, b):
#        clear_output()
#        root = Tk()
#        root.withdraw()
#        root.call('wm', 'attributes', '.', '-topmost', True)
#        b.files = filedialog.askopenfilename(multiple=True,
#                                             initialdir=os.path.join(self.settingsObject.workflow_folder, '2-soak'),
#                                             title="Select file",
#                                             filetypes=[("Text Files",
#                                                     "*xtal*.csv")])
#
#        if os.path.isfile(b.files[0]):
#            self.logger.info('loading ' + b.files[0])
#            for line in open(b.files[0]):
#                if line.startswith(';'):
#                    continue
#                xtal = re.split(r'[,;]+', line)[7]
#                puck = re.split(r'[,;]+', line)[11]
#                position = re.split(r'[,;]+', line)[12]
#
#                timestamp = re.split(r'[,;]+', line)[9]
#
#                barcode = re.split(r'[,;]+', line)[1]
#                row = re.split(r'[,;]+', line)[3]
#                column = '0' * (2 - len(re.split(r'[,;]+', line)[4])) + re.split(r'[,;]+', line)[4]
#                subwell = re.split(r'[,;]+', line)[5]
#                well = row + column
#        else:
#            self.logger.error('cannot read file ' + b.files[0])


    def import_crystal_soak_csv(self, b):
        #
        # query transferred compounds
        query = db.select([self.dbObject.soakplateTable.columns.SoakPlate.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        soakplates = [x[0] for x in ResultProxy.fetchall()]

        for soakPlate in soakplates:
            if os.path.isfile(os.path.join(workflow_folder, '2-soak', soakPlate + '.csv')):
                self.logger.info('found {0!s}.csv'.format(soakPlate))


            else:
                self.logger.warning('cannot find {0!s in {1!s}}'.format(soakPlate, os.path.join(workflow_folder, '2-soak')))

            # query soaked crystals


        #    for csv in glob.glob soaked crystals

            # write csv file in mount folder if respective file does not exist

    def update_crystal_soak_table(self, b):
        print('hallo')
