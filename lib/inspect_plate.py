import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
import sqlalchemy as db
import matplotlib.pyplot as plt
import misc
from beakerx import *

class inspect_plate(object):
    def __init__(self, settingsObject, dbObject, logger):
        self.logger = logger
        self.dbObject = dbObject
        self.settingsObject = settingsObject
        self.import_shifter_marked_crystals_button = widgets.Button(description='import marked crystals from shifter')
        self.import_shifter_marked_crystals_button.on_click(self.import_shifter_marked_crystals)

        n_rows_mounted_crystals = 288

        headerList_mounted_crystals = [
            'Crystal_ID',
            'CompoundBatch_ID',
            'Pin_Barcode',
            'Puck_Position',
            'Puck_Name',
            'Manual_Crystal_ID'
        ]

        x = []

        for i in range(n_rows_mounted_crystals):
            m = {}
            for j in range(len(headerList_mounted_crystals)):
                key = headerList_mounted_crystals[j]
                value = "............"  # cannot be space
                m[key] = value
            x.append(m)

        self.mounted_crystals_sheet = TableDisplay(x)

        self.vbox_cystal_image = widgets.VBox(children=[])


    def import_shifter_marked_crystals(self, b):
        clear_output()
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        b.files = filedialog.askopenfilename(multiple=True,
                                             initialdir=os.path.join(self.settingsObject.workflow_folder, '1-inspect'),
                                             title="Select file",
                                             filetypes=[("Text Files",
                                                         "*.csv")])

        wellList = []
        if os.path.isfile(b.files[0]):
            self.logger.info('loading ' + b.files[0])
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
                wellList.append(well + subwell)
        else:
            self.logger.error('cannot read file ' + b.files[0])

        self.show_marked_crystals(wellList)

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

    def show_marked_crystals(self, wellList):
        magnify = 2
        out = widgets.Output()
        fig, ax = plt.subplots()
        plt.xlim(0,36 * magnify)
        plt.ylim(0,25 * magnify)
        ax.set_aspect(1)
        for c in misc.swiss_ci_layout():
            well = c[0]
            x = c[1] * magnify
            y = c[2] * magnify
            radius = 0.2 * magnify
            if c[3] == 'circle' and well in wellList:
                ax.add_artist(plt.Circle((x, y), radius, color='red'))
            if c[3] == 'circle' and not well in wellList:
                ax.add_artist(plt.Circle((x, y), radius, color='gray'))
            elif c[3] == 'rectangle':
                ax.add_patch(Rectangle((x-radius, y-radius), radius*2, radius*2,edgecolor='black',facecolor='none',lw=0.2))
        plt.axis("off")
        with out:
            clear_output(wait=True)
            display(plt.show())
        self.vbox_cystal_image.children = [out]
