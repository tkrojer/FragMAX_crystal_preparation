import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
import sqlalchemy as db
#import matplotlib.pyplot as plt
import misc
from beakerx import *
import os
import re
import tips
from shutil import copyfile
from shutil import move
from datetime import datetime

class inspect_plate(object):
    def __init__(self, settingsObject, dbObject, logger):
        self.logger = logger
        self.dbObject = dbObject
        self.settingsObject = settingsObject
        self.import_shifter_marked_crystals_button = widgets.Button(description='import marked crystals from shifter',
                                                                    tooltip=tips.import_shifter_marked_crystals_button_tip())
        self.import_shifter_marked_crystals_button.on_click(self.import_shifter_marked_crystals)

        self.n_rows_inspected_wells = 288

        headerList_inspected_wells = [
            'CrystalPlate_Barcode',
            'CrystalPlate_Well',
            'CrystalPlate_Subwell'
        ]

        x = []
        for i in range(self.n_rows_inspected_wells):
            m = {}
            for j in range(len(headerList_inspected_wells)):
                key = headerList_inspected_wells[j]
                value = "............"  # cannot be space
                m[key] = value
            x.append(m)

        self.inspected_wells_sheet = TableDisplay(x)

#        self.vbox_cystal_image = widgets.VBox(children=[])


    def import_shifter_marked_crystals(self, b):
        clear_output()
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        b.files = filedialog.askopenfilename(multiple=True,
                                             initialdir=os.path.join(self.settingsObject.workflow_folder, '1-inspect'),
                                             title="Select file",
                                             filetypes=[("CSV Files",
                                                         ".csv")])

#        wellList = []
        if os.path.isfile(b.files[0]):
            if not b.files[0].endswith('_inspect.csv'):
                self.logger.error('selected filename is {0!s}, but file needs to end with _inspect.csv'.format(b.files[0]))
            else:
                self.logger.info('loading ' + b.files[0])
                n = 0
                for line in open(b.files[0]):
                    if line.startswith(';'):
                        continue
                    barcode = re.split(r'[ ,;]+', line)[1]
                    row = re.split(r'[ ,;]+', line)[3]
                    column = '0' * (2 - len(re.split(r'[ ,;]+', line)[4])) + re.split(r'[ ,;]+', line)[4]
                    subwell = re.split(r'[ ,;]+', line)[5]
                    well = row + column
                    marked_crystal_id = barcode + '-' + well + subwell
                    self.update_marked_crystal_in_db(marked_crystal_id, barcode, well, subwell)
#                    wellList.append(well + subwell)
                    self.inspected_wells_sheet.values[n][0] = barcode
                    self.inspected_wells_sheet.values[n][1] = well
                    self.inspected_wells_sheet.values[n][2] = subwell
                    n += 1
                self.inspected_wells_sheet.sendModel()
                if n < self.n_rows_inspected_wells:
                    for i in range(n,self.n_rows_inspected_wells):
                        self.inspected_wells_sheet.values[n][0] = "............"
                        self.inspected_wells_sheet.values[n][1] = "............"
                        self.inspected_wells_sheet.values[n][2] = "............"
                self.inspected_wells_sheet.sendModel()
                self.save_csv_file_to_soak_folder(b.files[0])
        else:
            self.logger.error('cannot read file ' + b.files[0])

#        self.show_marked_crystals(wellList)

    def update_marked_crystal_in_db(self, marked_crystal_id, barcode, well, subwell):
        query = db.select([self.dbObject.markedcrystalTable.columns.MarkedCrystal_ID.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        marked_crystals = [x[0] for x in ResultProxy.fetchall()]

        if marked_crystal_id in marked_crystals:
            self.logger.warning('crystal already flagged for soaking; skipping...')
        else:
            self.logger.info('marking crystal for soaking in database: ' + marked_crystal_id)
            values_list = [{
                'MarkedCrystal_ID':      marked_crystal_id,
                'CrystalPlate_Barcode':  barcode,
                'CrystalPlate_Well':     well,
                'CrystalPlate_Subwell':  subwell
                    }]
            query = db.insert(self.dbObject.markedcrystalTable)
            self.dbObject.connection.execute(query,values_list)

    def save_csv_file_to_soak_folder(self, shifter_csv):
        self.logger('saving copy of shifter csv file to 2-soak folder...')
        new_filename = shifter_csv.replace('_inspect.csv', '_crystal.csv')
        if os.path.isfile(os.path.join(self.settingsObject.workflow_folder, '2-soak', new_filename)):
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.logger.warning('file exists: {0!s}; moving existing file to backup folder'.format(new_filename))
            move(os.path.join(self.settingsObject.workflow_folder, '2-soak', new_filename),
                 os.path.join(self.settingsObject.workflow_folder, '2-soak', 'backup', new_filename + now))
        copyfile(os.path.join(self.settingsObject.workflow_folder, '1-inspect', shifter_csv),
                 os.path.join(self.settingsObject.workflow_folder, '2-soak', new_filename))

#    def show_marked_crystals(self, wellList):
#        magnify = 2
#        out = widgets.Output()
#        fig, ax = plt.subplots()
#        plt.xlim(0,36 * magnify)
#        plt.ylim(0,25 * magnify)
#        ax.set_aspect(1)
#        for c in misc.swiss_ci_layout():
#            well = c[0]
#            x = c[1] * magnify
#            y = c[2] * magnify
#            radius = 0.2 * magnify
#            if c[3] == 'circle' and well in wellList:
#                ax.add_artist(plt.Circle((x, y), radius, color='red'))
#            if c[3] == 'circle' and not well in wellList:
#                ax.add_artist(plt.Circle((x, y), radius, color='gray'))
#            elif c[3] == 'rectangle':
#                ax.add_patch(Rectangle((x-radius, y-radius), radius*2, radius*2,edgecolor='black',facecolor='none',lw=0.2))
#        plt.axis("off")
#        with out:
#            clear_output(wait=True)
#            display(plt.show())
#        self.vbox_cystal_image.children = [out]
