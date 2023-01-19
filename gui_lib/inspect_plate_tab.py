import ipywidgets as widgets
#from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
#from beakerx import *
#import beakerx
import os
#import re
#import tips
#from shutil import copyfile
#from shutil import move
#from datetime import datetime
import ntpath

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import filesystem as fs
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query

import pandas as pd
import panel as pn
import numpy as np
pn.extension('tabulator')

class inspect_plate_tab(object):
    def __init__(self, settingsObject, dbObject, logger):
        self.logger = logger
        self.dbObject = dbObject
        self.settingsObject = settingsObject

        self.import_shifter_marked_crystals_button = widgets.Button(description='import marked crystals from shifter')
        self.import_shifter_marked_crystals_button.on_click(self.import_shifter_marked_crystals)

        self.n_rows_inspected_wells = 288

        sheet_header = [
            'crystal_plate_barcode',
            'crystal_plate_well',
            'crystal_plate_subwell'
        ]

#        x = []
#        for i in range(self.n_rows_inspected_wells):
#            m = {}
#            for j in range(len(headerList_inspected_wells)):
#                key = headerList_inspected_wells[j]
#                value = "............"  # cannot be space
#                m[key] = value
#            x.append(m)
#        print(x)
#        self.inspected_wells_sheet = beakerx.TableDisplay(x)
        data = []
        for i in range(self.n_rows_inspected_wells):
            row = []
            for j in range(len(sheet_header)):
                row.append("............")
            data.append(row)
#        data = [['tom', 10], ['nick', 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=[sheet_header])

        out = widgets.Output()
        self.inspected_wells_sheet = pn.widgets.Tabulator(df)
        self.table_box = widgets.VBox()
        with out:
            clear_output(wait=True)
            display(self.inspected_wells_sheet)
        self.table_box.children = [out]


#        self.vbox_cystal_image = widgets.VBox(children=[])

#    def get_crystal_screen_name(self, barcode):
#        query = db.select([self.dbObject.crystalplateTable.columns.CrystalScreen_Name]).where(
#            self.dbObject.crystalplateTable.columns.CrystalPlate_Barcode == barcode)
#        ResultProxy = self.dbObject.connection.execute(query)
#        try:
#            screen_name = ResultProxy.fetchall()[0][0]
#            self.logger.info('--> {0!s}'.format(screen_name))
#        except IndexError:
#            screen_name = ''
#        return screen_name


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
        shiftercsv = b.files[0]
        if os.path.isfile(shiftercsv):
            if not shiftercsv.endswith('_inspect.csv'):
                self.logger.error('selected filename is {0!s}, but file needs to end with _inspect.csv'.format(shiftercsv))
            else:
                xtal_list = fs.import_marked_crystals_from_shifter_csv(self.logger, shiftercsv)
                self.update_inspected_wells_sheet(xtal_list)
                query.save_marked_crystals_to_db(self.dal, self.logger, xtal_list)
                folder = self.settingsObject.workflow_folder
                query.save_marked_crystals_to_soak_folder_as_shifter_csv(self.logger, shiftercsv, folder)
        else:
            self.logger.error('cannot read file ' + b.files[0])


    def update_inspected_wells_sheet(self, xtal_list):
        self.logger.info('updating inspected_wells_sheet widget')
        n = 0
        data = []
        for xtal in xtal_list:
            data.append([xtal['crystal_plate_barcode'], xtal['crystal_plate_well'], xtal['crystal_plate_subwell']])
#            self.inspected_wells_sheet.values[n][0] = xtal['crystal_plate_barcode']
#            self.inspected_wells_sheet.values[n][1] = xtal['crystal_plate_well']
#            self.inspected_wells_sheet.values[n][2] = xtal['crystal_plate_subwell']
            n += 1
#        self.inspected_wells_sheet.sendModel()
        if n < self.n_rows_inspected_wells:
#            for i in range(n, self.n_rows_inspected_wells):
            for i in range(n, self.n_rows_inspected_wells):
                data.append(["............", "............", "............"])
#                self.inspected_wells_sheet.values[i][0] = "............"
#                self.inspected_wells_sheet.values[i][1] = "............"
#                self.inspected_wells_sheet.values[i][2] = "............"
#        self.inspected_wells_sheet.sendModel()

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
