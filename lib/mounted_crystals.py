import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
import sqlalchemy as db
import pandas as pd
from beakerx import *

class mounted_crystals(object):
    def __init__(self, settingsObject, dbObject, logger):

        self.settingsObject = settingsObject

        self.dbObject = dbObject

        self.logger = logger

        n_rows_mounted_crystals = 1000

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
                value = "............"     # cannot be space
                m[key] = value
            x.append(m)

        self.mounted_crystals_sheet = TableDisplay(x)

        self.grid_widget = widgets.GridspecLayout(2, 5)

#        self.grid_widget[0:8,0:3] = self.mounted_crystals_sheet

        update_mounted_crystal_table_button = widgets.Button(description='Update table')
        update_mounted_crystal_table_button.on_click(self.update_mounted_crystal_table)
        self.grid_widget[0,0] = update_mounted_crystal_table_button

        import_mounted_crystals_button = widgets.Button(description='Import from Shifter')
        import_mounted_crystals_button.on_click(self.import_mounted_crystals)
        self.grid_widget[0,1] = import_mounted_crystals_button

        import_manually_mounted_crystals_button = widgets.Button(description='Import manual')
#        import_manually_mounted_crystals_button.on_click(self.import_manually_mounted_crystals)
        self.grid_widget[0,2] = import_manually_mounted_crystals_button

        save_template_manually_mounted_crystals_button = widgets.Button(description='Save manual template')
#        save_template_manually_mounted_crystals_button.on_click(self.save_template_manually_mounted_crystals)
        self.grid_widget[0,3] = save_template_manually_mounted_crystals_button

        export_csv_for_exi_button = widgets.Button(description='Export CSV for EXI')
        #export_csv_for_exi_button.on_click(self.export_csv_for_exi)
        self.grid_widget[0,4] = export_csv_for_exi_button

    def update_mounted_crystal_table(self, b):
        query = db.select([self.dbObject.mountedcrystalTable.columns.Crystal_ID,
                             self.dbObject.mountedcrystalTable.columns.CompoundBatch_ID,
                             self.dbObject.mountedcrystalTable.columns.Pin_Barcode,
                             self.dbObject.mountedcrystalTable.columns.Puck_Position,
                             self.dbObject.mountedcrystalTable.columns.Puck_Name,
                             self.dbObject.mountedcrystalTable.columns.Manual_Crystal_ID]).order_by(
                             self.dbObject.mountedcrystalTable.columns.Crystal_ID.asc())
        df = pd.read_sql_query(query, self.dbObject.engine)
        for index, row in df.iterrows():
            self.mounted_crystals_sheet.updateCell(index,"Crystal_ID",df.at[index,'Crystal_ID'])
            if df.at[index,'CompoundBatch_ID'] is None:
                self.mounted_crystals_sheet.values[index][1] = 'None'
            else:
                self.mounted_crystals_sheet.values[index][1] = df.at[index,'CompoundBatch_ID']
            self.mounted_crystals_sheet.values[index][2] = df.at[index,'Pin_Barcode']
            self.mounted_crystals_sheet.values[index][3] = df.at[index,'Puck_Position']
            self.mounted_crystals_sheet.values[index][4] = df.at[index,'Puck_Name']
            self.mounted_crystals_sheet.values[index][5] = df.at[index,'Manual_Crystal_ID']
        self.mounted_crystals_sheet.sendModel()


    def import_mounted_crystals(self, b):
        clear_output()
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        b.files = filedialog.askopenfilename(multiple=True,
                                             initialdir=os.path.join(self.settingsObject.workflow_folder, '3-mount'),
                                             title="Select file",
                                             filetypes=[("Text Files",
                                                     "*.csv")])

        if os.path.isfile(b.files[0]):
            self.logger.info('loading ' + b.files[0])
            df = pd.DataFrame()
            for line in open(b.files[0]):
                if line.startswith(';'):
                    continue
                plate_name = re.split(r'[,;]+', line)[1]
                plate_row = re.split(r'[,;]+', line)[3]
                plate_column = '0' * (2 - len(re.split(r'[,;]+', line)[4])) + re.split(r'[,;]+', line)[4]
                plate_subwell = re.split(r'[,;]+', line)[5]
                mount_time = re.split(r'[,;]+', line)[9]
                comment = re.split(r'[,;]+', line)[6]

#        "Crystal_ID"
#        "Pin_Barcode"
#        "Puck_Name"
#        "Puck_Position"
#        "Status"
#        "Mount_Date"
#        "Soak_ID"
#        "Cryo"
#        "Cryo_Concentration"
#        "CompoundBatch_ID"
#        "Comment"
#        "Manual_Crystal_ID"

        else:
            logger.error('cannot read file ' + b.files[0])


    def insert_mounted_crystals_in_db(self, df):

        proteinacronym = None
        # query protein acronym
        if proteinacronym is None:
            self.logger.error('Please enter and save protein acronym in "Project Description" tab and then try again')
            pass
        else:
            self.logger.info('protein acronym is {0!s}'.format(proteinacronym))

        query = db.select([self.dbObject.mountedcrystalTable.columns.Manual_Crystal_ID.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_manually_mounted_crystals = [x[0] for x in ResultProxy.fetchall()]

        query = db.select([self.dbObject.markedcrystalTable.columns.MarkedCrystal_ID.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        marked_crystals = [x[0] for x in ResultProxy.fetchall()]

        # latest crystal ID
        query = db.select([self.dbObject.mountedcrystalTable.columns.Crystal_ID.distinct()]).order_by(
            self.dbObject.mountedcrystalTable.columns.Crystal_ID.desc()).limit(1)
        ResultProxy = self.dbObject.connection.execute(query)
        last_crystal_id = ResultProxy.fetchall()[0][0]
        next_crystal_number = int(last_crystal_id.split('-')[1].replace('x', '')) + 1

        for index, row in df.iterrows():
            Manual_Crystal_ID = df.at[index, 'Manual_ID']

            barcode = df.at[index, 'CrystalPlate_Barcode']
            query = db.select([crystalplateTable.columns.CrystalPlate_Barcode.distinct()])
            ResultProxy = connection.execute(query)
            existing_crystal_plates = [x[0] for x in ResultProxy.fetchall()]
            if barcode not in existing_crystal_plates:
                logger.error(
                    'barcode {0!s} not registered in database; please add crystal plate before registering mounted crystals...'.format(
                        barcode))
                continue

            try:
                if len(df.at[index, 'CrystalPlate_Well']) == 2:
                    well = df.at[index, 'CrystalPlate_Well'][0] + '0' + df.at[index, 'CrystalPlate_Well'][1]
                else:
                    well = df.at[index, 'CrystalPlate_Well']
                subwell = df.at[index, 'CrystalPlate_Subwell']
                marked_crystal_id = barcode + '-' + well + subwell
                if marked_crystal_id not in marked_crystals:
                    logger.info('marking crystal for mounting/ soaking in database: ' + marked_crystal_id)
                    values_list = [{
                        'MarkedCrystal_ID': marked_crystal_id,
                        'CrystalPlate_Barcode': barcode,
                        'CrystalPlate_Well': well,
                        'CrystalPlate_Subwell': subwell
                    }]
                    query = db.insert(markedcrystalTable)
                    ResultProxy = connection.execute(query, values_list)
            except TypeError:
                logger.error(
                    'there is something wrong with well and/ or subwell description: well = {0!s}, subwell = {1!s}; please correct!'.format(
                        df.at[index, 'CrystalPlate_Well'], df.at[index, 'CrystalPlate_Subwell']))
                continue

            if Manual_Crystal_ID in existing_manually_mounted_crystals:
                logger.warning('updating records for manually mounted crystal: {0!s}'.format(well, condition))
                query = db.update(mountedcrystalTable).values(
                    Pin_Barcode=df.at[index, 'Pin_Barcode'],
                    Puck_Name=df.at[index, 'Puck_Name'],
                    Puck_Position=df.at[index, 'Puck_Position'],
                    CompoundBatch_ID=df.at[index, 'CompoundBatch_ID'],
                    Cryo=df.at[index, 'Cryo'],
                    Cryo_Concentration=df.at[index, 'Cryo_Concentration'],
                    Comment=df.at[index, 'Comment']
                ).where(
                    mountedcrystalTable.columns.Manual_Crystal_ID == Manual_Crystal_ID)
                results = connection.execute(query)
            else:
                Crystal_ID = str(proteinacronym) + '-x' + '0' * (4 - len(str(next_crystal_number))) + str(
                    next_crystal_number)
                logger.info('inserting new records for manually mounted crystal: {0!s} as {1!s}'.format(Manual_Crystal_ID,
                                                                                                    Crystal_ID))
                values_list = [{
                    'Manual_Crystal_ID': Manual_Crystal_ID,
                    'Crystal_ID': Crystal_ID,
                    'Pin_Barcode': df.at[index, 'Pin_Barcode'],
                    'Puck_Name': df.at[index, 'Puck_Name'],
                    'Puck_Position': df.at[index, 'Puck_Position'],
                    'CompoundBatch_ID': df.at[index, 'CompoundBatch_ID'],
                    'Cryo': df.at[index, 'Cryo'],
                    'Cryo_Concentration': df.at[index, 'Cryo_Concentration'],
                    'Comment': df.at[index, 'Comment']
                }]
                query = db.insert(mountedcrystalTable)
                ResultProxy = connection.execute(query, values_list)

                next_crystal_number += 1
