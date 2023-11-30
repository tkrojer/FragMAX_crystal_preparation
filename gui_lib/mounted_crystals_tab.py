import ipywidgets as widgets
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
from datetime import datetime

import panel as pn
pn.extension('tabulator')

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import mounted_crystals_fs as fs
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query
import mounted_crystals_db as db

class mounted_crystals_tab(object):
    def __init__(self, settingsObject, dal, logger, pgbar):

        self.settingsObject = settingsObject
        self.dal = dal
        self.logger = logger
        self.pgbar = pgbar

        self.grid_widget = widgets.GridspecLayout(10, 4)

        update_mounted_crystal_table_button = widgets.Button(description='Update table',
                                                             layout=widgets.Layout(display="flex", width="auto"))
        update_mounted_crystal_table_button.on_click(self.update_mounted_crystal_table)
        self.grid_widget[0, 0] = update_mounted_crystal_table_button

        import_mounted_crystals_button = widgets.Button(description='Import from Shifter',
                                                        layout=widgets.Layout(display="flex", width="auto"))
        import_mounted_crystals_button.on_click(self.shifter_mounted_crystals)
        self.grid_widget[0, 1] = import_mounted_crystals_button

        import_manually_mounted_crystals_button = widgets.Button(description='Import manual',
                                                                 layout=widgets.Layout(display="flex", width="auto"))
        import_manually_mounted_crystals_button.on_click(self.manual_mounted_crystals)
        self.grid_widget[0, 2] = import_manually_mounted_crystals_button

        save_template_manually_mounted_crystals_button = widgets.Button(description='Save manual template',
                                                                        layout=widgets.Layout(display="flex", width="auto"))
        save_template_manually_mounted_crystals_button.on_click(self.save_template_manually_mounted_crystals)
        self.grid_widget[0, 3] = save_template_manually_mounted_crystals_button

        export_csv_for_exi_button = widgets.Button(description='Export CSV for EXI',
                                                   layout=widgets.Layout(display="flex", width="auto"))
        export_csv_for_exi_button.on_click(self.export_csv_for_exi)
        self.grid_widget[1, 0] = export_csv_for_exi_button

        export_csv_for_fragmaxapp_button = widgets.Button(description='Export CSV for FragMAXapp',
                                                          layout=widgets.Layout(display="flex", width="auto"))
        export_csv_for_fragmaxapp_button.on_click(self.export_csv_for_fragmaxapp)
        self.grid_widget[1, 1] = export_csv_for_fragmaxapp_button

        export_csv_summary_button = widgets.Button(description='Export summary CSV',
                                                   layout=widgets.Layout(display="flex", width="auto"))
        export_csv_summary_button.on_click(self.export_csv_summary)
        self.grid_widget[1, 2] = export_csv_summary_button

        self.table_box = widgets.VBox()
        self.get_values_for_mounted_crystal_table()
        self.grid_widget[2:,0:] = self.table_box

    def shifter_mounted_crystals(self, b):
        folder = '3-mount'
        self.import_mounted_crystals(folder, b)

    def manual_mounted_crystals(self, b):
        folder = '4-mount-manual'
        self.import_mounted_crystals(folder, b)

    def import_mounted_crystals(self, folder, b):
        clear_output()
        root = Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        b.files = filedialog.askopenfilename(multiple=True,
                                             initialdir=os.path.join(self.settingsObject.workflow_folder, folder),
                                             title="Select file",
                                             filetypes=[("Text Files", "*.csv"), ("Excel file","*.xlsx")])
        if folder == '3-mount':
            for f in b.files:
                self.logger.info('reading CSV file of shifter mounted crystals from CSV file: ' + f)
                self.read_shifter_csv(f)
        elif folder == '4-mount-manual':
            for f in b.files:
                self.logger.info('reading EXCEL file of manually mounted crystals: ' + b.files[0])
                self.read_manual_excel_file(f)
#            df = pd.read_csv(b.files[0], sep=';')
#            self.logger.info(df.head)
#            self.update_db_with_manually_mounted_crystals(df)

    def save_template_manually_mounted_crystals(self, b):
        self.logger.info('saving CSV file for manually mounted crystals in workflow/4-mount-manual...')
        now_ext = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = os.path.join(self.settingsObject.workflow_folder, '4-mount-manual')
        excel_file = os.path.join(folder, 'manual_mount_' + now_ext + '.xlsx')
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        fs.save_manual_mount_template(self.logger, folder, now, excel_file)

    def read_shifter_csv(self, shifter_csv_file):
        xtal_list, soak_list = fs.get_shifter_csv_file_as_dict_list(self.logger, shifter_csv_file)
        self.update_database(xtal_list, soak_list)

    def read_manual_excel_file(self, manual_excel_file):
        xtal_list, soak_list = fs.get_manual_excel_file_as_dict_list(self.logger, manual_excel_file)
        self.update_database(xtal_list, soak_list)

    def update_database(self, xtal_list, soak_list):
        proteinacronym = query.get_protein_acronym(self.dal, self.logger)
        self.logger.info('proteinacronym: {0!s}'.format(proteinacronym))
        if xtal_list:
            db.save_mounted_crystals_to_database(self.logger, self.dal, xtal_list, proteinacronym, self.pgbar)
        if soak_list:
            db.update_soeked_crystal_table(self.logger, self.dal, soak_list, self.pgbar)

    def update_mounted_crystal_table(self, b):
        self.get_values_for_mounted_crystal_table()

    def get_values_for_mounted_crystal_table(self):
        df = db.get_mounted_crystals_from_db_for_table_as_df(self.logger, self.dal)
        out = widgets.Output()
        mounted_crystal_table = pn.widgets.Tabulator(df)
        with out:
            clear_output(wait=True)
            display(mounted_crystal_table)
            self.table_box.children = [out]

    def export_csv_for_exi(self, b):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        shipment = 'shipment_' + now
        df = db.get_mounted_crystals_for_exi_where_shipment_is_none(self.logger, self.dal)
        fs.save_csv_file_for_exi(self.logger, df,
                                 os.path.join(self.settingsObject.workflow_folder, '5-exi', shipment + '.csv'))
        db.update_db_with_shipment_information(self.logger, self.dal, shipment)

    def export_csv_summary(self, b):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        summary = 'summary_' + now
        df = db.get_summary_dataframe(self.logger, self.dal)
        fs.save_csv_summary_file(self.logger, df,
                                 os.path.join(self.settingsObject.workflow_folder, '7-summary', summary + '.csv'))

    def export_csv_for_fragmaxapp(self, b):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fragmaxapp = 'fragmaxapp_' + now
        df = db.get_fragmax_dataframe(self.logger, self.dal)
        fs.save_csv_file_for_fragmaxapp(self.logger, df,
                                 os.path.join(self.settingsObject.workflow_folder, '6-fragmaxapp', fragmaxapp + '.csv'))







#    def reset_mounted_crystal_table(self):
#        self.logger.info('resetting table...')
#        for i in range(self.n_rows_mounted_crystals):
#            for n in range(len(self.headerList_mounted_crystals)):
#                self.mounted_crystals_sheet.values[i][n] = "............"
#        self.mounted_crystals_sheet.sendModel()

#    def get_mounted_crystals_from_db(self):
#        self.logger.info('fetching mounted crystal information from database...')
#        query = db.select([self.dbObject.mountedcrystalTable.columns.Crystal_ID,
#                           self.dbObject.soakplateTable.columns.CompoundBatch_ID,
#                           self.dbObject.mountedcrystalTable.columns.Pin_Barcode,
#                           self.dbObject.mountedcrystalTable.columns.Puck_Position,
#                           self.dbObject.mountedcrystalTable.columns.Puck_Name,
#                           self.dbObject.mountedcrystalTable.columns.Manual_Crystal_ID]
#                          ).order_by(
#                           self.dbObject.mountedcrystalTable.columns.Crystal_ID.asc())
#
#        query = query.select_from(self.dbObject.joined_tables)
#
#        ResultProxy = self.dbObject.connection.execute(query)
#        result = ResultProxy.fetchall()
#        return result


#    def update_mounted_crystal_table(self, b):
#        self.reset_mounted_crystal_table()
#        result = self.get_mounted_crystals_from_db()
#
#        for i in range(len(result)):
#            for n in range(len(self.headerList_mounted_crystals)):
#                self.mounted_crystals_sheet.values[i][n] = result[i][n]
#        self.mounted_crystals_sheet.sendModel()


#    def update_shipment_in_db(self, shipment, Crystal_ID):
#        self.logger.info('updating shipment information for {0!s} in DB: {1!s}'.format(Crystal_ID, shipment))
#        query = db.update(self.dbObject.mountedcrystalTable).values(Shipment=shipment).where(
#            self.dbObject.mountedcrystalTable.columns.Crystal_ID == Crystal_ID)
#        self.dbObject.connection.execute(query)

#    def save_shipment_csv_file(self, shipment, exi_csv):
#        if exi_csv != '':
#            self.logger.info('saving CSV file for upload to EXI: {0!s}'.format(
#                os.path.join(self.settingsObject.workflow_folder, '5-exi', shipment + '.csv')))
#            f = open(os.path.join(self.settingsObject.workflow_folder, '5-exi', shipment + '.csv'), 'w')
#            f.write(exi_csv)
#            f.close()
#        else:
#            self.logger.error('CSV file is empty; aborting save...')



#    def save_fragmax_csv_file(self, shipment, fragmax_csv):
#        if fragmax_csv != '':
#            self.logger.info('trying to save CSV file for upload to FragMAXapp: {0!s}'.format(
#                os.path.join(self.settingsObject.workflow_folder, '6-fragmaxapp', shipment + '.csv')))
#            if os.path.isfile(os.path.join(self.settingsObject.workflow_folder, '6-fragmaxapp', shipment + '.csv')):
#                self.logger.error('CSV file exists; skipping...')
#            else:
#                self.logger.info('saving CSV file...')
#                f = open(os.path.join(self.settingsObject.workflow_folder, '6-fragmaxapp', shipment + '.csv'), 'w')
#                f.write(fragmax_csv)
#                f.close()
#        else:
#            self.logger.error('CSV file is empty; aborting save...')


#    def export_csv_for_fragmaxapp(self, b):
#        self.logger.info('preparing CSV file for upload to FragMAXapp...')
#
#        query = db.select([
#            self.dbObject.mountedcrystalTable.columns.Crystal_ID,
#            self.dbObject.mountedcrystalTable.columns.Shipment,
#            self.dbObject.compoundbatchTable.columns.Compound_ID,
#            self.dbObject.compoundbatchTable.columns.Library_Name,
#            self.dbObject.crystalscreenTable.columns.CrystalScreen_Condition,
#            self.dbObject.mountedcrystalTable.columns.Mount_Date,
#            self.dbObject.soakedcrystalTable.columns.Soak_Time,
#            self.dbObject.crystalplateTable.columns.Temperature,
#            self.dbObject.crystalplateTable.columns.Crystallization_Method
#            ]).where(self.dbObject.mountedcrystalTable.columns.Shipment != None).order_by(
#            self.dbObject.mountedcrystalTable.columns.Crystal_ID)

#        query = query.select_from(self.dbObject.joined_tables)


#        ResultProxy = self.dbObject.connection.execute(query)
#        crystals = ResultProxy.fetchall()
#        fragmax_csv = 'SampleID,FragmentLibrary,FragmentCode\n'
#        shipmentList = []
#        foundCrystals = False
#        for c in crystals:
#            foundCrystals = True
#            crystalID = c[0]
#            shipment = c[1]
#            compound = c[2]
#            if not compound:
#                # manually mounted crystals have a compound ID in the mounted crystal table
##                query = db.select([
##                    self.dbObject.mountedcrystalTable.columns.CompoundBatch_ID
##                ]).where(self.dbObject.mountedcrystalTable.columns.Crystal_ID == crystalID)
##                ResultProxy = self.dbObject.connection.execute(query)
##                cpdID = ResultProxy.fetchall()
#                compound = ''
#            library = c[3]
#            if not library:
#                library = ''
#            condition = c[4]
#            temperature = str(c[7])
#            method = c[8]
#            try:
#                soak_start = datetime.strptime(c[5], '%d/%m/%Y %H:%M:%S')
#                soak_end = datetime.strptime(c[6], '%d/%m/%Y %H:%M:%S')
#                diff = soak_end - soak_start
#                soak_time = str(int(diff.total_seconds()))
#            except TypeError:
#                soak_time = '0'
#            if not shipmentList:
#                shipmentList.append(shipment)
#            if shipment not in shipmentList:
#                self.save_fragmax_csv_file(shipmentList[len(shipmentList)-2], fragmax_csv)
#                shipmentList.append(shipment)
#                fragmax_csv = 'SampleID,FragmentLibrary,FragmentCode\n'
#            fragmax_csv += '{0!s},{1!s},{2!s}\n'.format(crystalID, library, compound)
#        if fragmax_csv:
#            self.save_fragmax_csv_file(shipment, fragmax_csv)
#        if not foundCrystals:
#            self.logger.error('did not find any crystals, make sure that you exported samples for EXI!')


#    def get_all_soaked_crystals(self):
#        joined_soakedcrystalTable = self.dbObject.soakedcrystalTable.join(
#            self.dbObject.soakplateTable, self.dbObject.soakedcrystalTable.columns.SoakPlate_Condition_ID ==
#                                  self.dbObject.soakplateTable.columns.SoakPlate_Condition_ID, isouter=True).join(
#            self.dbObject.compoundbatchTable, self.dbObject.soakplateTable.columns.CompoundBatch_ID ==
#                                      self.dbObject.compoundbatchTable.columns.CompoundBatch_ID, isouter=True).join(
#            self.dbObject.compoundTable, self.dbObject.compoundbatchTable.columns.Compound_ID ==
#                                 self.dbObject.compoundTable.columns.Compound_ID, isouter=True)
#
#        query = db.select([
#            self.dbObject.soakedcrystalTable.columns.Soak_ID,
#            self.dbObject.compoundbatchTable.columns.Compound_ID,
#            self.dbObject.compoundTable.columns.Smiles,
#            self.dbObject.compoundTable.columns.Vendor_ID,
#            self.dbObject.compoundTable.columns.Vendor,
#            self.dbObject.compoundbatchTable.columns.Library_Name,
#            self.dbObject.soakedcrystalTable.columns.Soak_Time,
#            self.dbObject.soakedcrystalTable.columns.Soak_Comment
#        ]).order_by(
#            self.dbObject.soakedcrystalTable.columns.Soak_ID)
#
#        query = query.select_from(joined_soakedcrystalTable)
#        ResultProxy = self.dbObject.connection.execute(query)
#        soaks = ResultProxy.fetchall()
#        return soaks


#    def get_all_mounted_crystals(self):
#        query = db.select([
#            self.dbObject.mountedcrystalTable.columns.Crystal_ID,
#            self.dbObject.compoundbatchTable.columns.Compound_ID,
#            self.dbObject.compoundTable.columns.Smiles,
#            self.dbObject.compoundTable.columns.Vendor_ID,
#            self.dbObject.compoundTable.columns.Vendor,
#            self.dbObject.compoundbatchTable.columns.Library_Name,
#            self.dbObject.crystalscreenTable.columns.CrystalScreen_Condition,
#            self.dbObject.mountedcrystalTable.columns.Mount_Date,
#            self.dbObject.soakedcrystalTable.columns.Soak_Time,
#            self.dbObject.crystalplateTable.columns.Temperature,
#            self.dbObject.crystalplateTable.columns.Crystallization_Method,
#            self.dbObject.mountedcrystalTable.columns.Manual_Crystal_ID,
#            self.dbObject.mountedcrystalTable.columns.CompoundBatch_ID,
#            self.dbObject.mountedcrystalTable.columns.Comment,
#            self.dbObject.soakedcrystalTable.columns.Soak_ID,
#            self.dbObject.soakedcrystalTable.columns.Soak_Comment
#        ]).order_by(
#            self.dbObject.mountedcrystalTable.columns.Crystal_ID)
#
#        query = query.select_from(self.dbObject.joined_tables)
#        ResultProxy = self.dbObject.connection.execute(query)
#        crystals = ResultProxy.fetchall()
#        return crystals


#    def add_mounted_crystals_to_csv(self, crystals, csvOut):
#        Soak_ID_list = []
#        for c in crystals:
#            crystalID = c[0]
#
#            cpdID = c[1]
#            if not cpdID:
#                cpdID = ''
#
#            smiles = c[2]
#            if not smiles:
#                smiles = ''
#
#            vendor_id = c[3]
#            if not vendor_id:
#                vendor_id = ''
#
#            vendor = c[4]
#            if not vendor:
#                vendor = ''
#
#            try:
#                soak_start = datetime.strptime(c[8], '%d/%m/%Y %H:%M:%S')
#                soak_end = datetime.strptime(c[7], '%d/%m/%Y %H:%M:%S')
#                diff = soak_end - soak_start
#                soak_time = str(round((float(diff.total_seconds())/3600), 1))
#            except TypeError:
#                soak_time = ''
#
#            condition = c[6]
#            if not condition:
#                condition = ''
#
#            manual_id = str(c[11])
#            if not manual_id:
#                manual_id = ''
#
#            manual_cpd = str(c[12])
#            if not manual_cpd:
#                manual_cpd = ''
#
#            comment = str(c[13]).split(':')[2]
#            if not comment:
#                comment = ''
#            elif comment == 'No comment':
#                comment = 'OK'
#
#            cpd_behaviour = str(c[15]).split(':')[1]
#            if not cpd_behaviour:
#                cpd_behaviour = ''
#            elif cpd_behaviour == 'No comment':
#                cpd_behaviour = 'clear'
#
#            csvOut += crystalID + ',' + cpdID + ',' + smiles + ',' + vendor_id + ',' + vendor + ',' + soak_time + ',' + condition + ',' + manual_id + ',' + manual_cpd + ',' + comment + ',' + cpd_behaviour + '\n'
#
#            Soak_ID_list.append(str(c[14]))
#        return csvOut, Soak_ID_list


#    def add_failed_soaks_to_csv(self, soaks, csvOut, Soak_ID_list):
#
#        for s in soaks:
#            soak_id = s[0]
#            if soak_id not in Soak_ID_list:
#                cpdID = s[1]
#                if not cpdID:
#                    cpdID = ''
#
#                smiles = s[2]
#                if not smiles:
#                    smiles = ''
#
#                vendor_id = s[3]
#                if not vendor_id:
#                    vendor_id = ''
#
#                vendor = s[4]
#                if not vendor:
#                    vendor = ''
#
#                condition = s[6]
#                if not condition:
#                    condition = ''
#
#                cpd_behaviour = str(s[7]).split(':')[1]
#                if not cpd_behaviour:
#                    cpd_behaviour = ''
#                elif cpd_behaviour == 'No comment':
#                    cpd_behaviour = 'clear'
#
#                csvOut += 'nan,' + cpdID + ',' + smiles + ',' + vendor_id + ',' + vendor + ',nan,' + condition + ',nan,nan,nan,' + cpd_behaviour + '\n'
#        return csvOut


#    def export_csv_summary(self, b):
#        crystals = self.get_all_mounted_crystals()
#        soaks = self.get_all_soaked_crystals()
#
#        self.logger.error(crystals)
#        csvOut = ''
#        csvOut += 'SampleID,CompoundID,Smiles,VendorID,Vendor,SoakTime(h),CrystallizationCondition,ManualCrystalID,ManualCompoundID,CompoundBehaviour,CrystalBehaviourt\n'
#
#        csvOut, Soak_ID_list = self.add_mounted_crystals_to_csv(crystals, csvOut)
#        csvOut = self.add_failed_soaks_to_csv(soaks, csvOut, Soak_ID_list)
#
#        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#        self.logger.info('saving CSV summary {0!s}'.format(
#            os.path.join(self.settingsObject.workflow_folder, '7-summary', 'summary_' + now + '.csv')))
#        f = open(os.path.join(self.settingsObject.workflow_folder, '7-summary', 'summary_' + now + '.csv'), 'w')
#        f.write(csvOut)
#        f.close()

#    def save_template_manually_mounted_crystals(self, b):
#        self.logger.info('saving CSV file for manually mounted crystals in workflow/4-mount-manual...')
#        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#        csvHeader = 'Manual_Crystal_ID;CompoundBatch_ID;Puck_Name;Puck_Position;Pin_Barcode;Mount_Date;Cryo;Cryo_Concentration;CrystalPlate_Barcode;CrystalPlate_Well;CrystalPlate_Subwell;Comment\n'
#        f = open(os.path.join(self.settingsObject.workflow_folder, '4-mount-manual', 'mount_' + now + '.csv'), 'w')
#        f.write(csvHeader)
#        f.close()

#    def get_known_plate_types(self):
#        self.logger.info('reading known plate types from database...')
#        query = db.select([self.dbObject.crystal_plate_typeTable.columns.Plate_Name.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        known_plate_types = [x[0] for x in ResultProxy.fetchall()]
#        self.logger.info('found the following plate types in database: {0!s}'.format(known_plate_types))
#        return known_plate_types

#    def update_markedcrystalTable(self, marked_crystal_id, barcode, well, subwell):
#        query = db.select([self.dbObject.markedcrystalTable.columns.MarkedCrystal_ID.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        marked_crystals = [x[0] for x in ResultProxy.fetchall()]
#
#        if marked_crystal_id not in marked_crystals:
#            self.logger.info('marking crystal for mounting/ soaking in database: ' + marked_crystal_id)
#            values_list = [{
#                'MarkedCrystal_ID': marked_crystal_id,
#                'CrystalPlate_Barcode': barcode,
#                'CrystalPlate_Well': well,
#                'CrystalPlate_Subwell': subwell
#            }]
#            query = db.insert(self.dbObject.markedcrystalTable)
#            self.dbObject.connection.execute(query, values_list)
#        else:
#            self.logger.info('marked crystal entry {0!a} exists in database'.format(marked_crystal_id))

#    def update_db_with_manually_mounted_crystals(self, df):
#
#        proteinacronym = self.get_protein_acronym()
#        if proteinacronym is None:
#            self.logger.error('Please enter and save protein acronym in "Project Description" tab and then try again')
#            pass
#        else:
#            self.logger.info('protein acronym is {0!s}'.format(proteinacronym))
#
#        query = db.select([self.dbObject.mountedcrystalTable.columns.Manual_Crystal_ID.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        existing_manually_mounted_crystals = [x[0] for x in ResultProxy.fetchall()]
#
#        query = db.select([self.dbObject.markedcrystalTable.columns.MarkedCrystal_ID.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        marked_crystals = [x[0] for x in ResultProxy.fetchall()]
#
#        # latest crystal ID
#        last_crystal_id = self.get_last_crystal_id(proteinacronym)
#        next_crystal_number = int(last_crystal_id.split('-')[1].replace('x', '')) + 1
#
#        for index, row in df.iterrows():
#            Manual_Crystal_ID = df.at[index, 'Manual_Crystal_ID']
#
#            barcode = df.at[index, 'CrystalPlate_Barcode']
#            query = db.select([self.dbObject.crystalplateTable.columns.CrystalPlate_Barcode.distinct()])
#            ResultProxy = self.dbObject.connection.execute(query)
#            existing_crystal_plates = [x[0] for x in ResultProxy.fetchall()]
#            if barcode not in existing_crystal_plates:
#                self.logger.error(
#                    'barcode {0!s} not registered in database; please add crystal plate before registering mounted crystals...'.format(
#                        barcode))
#                continue
#
#            try:
#                self.logger.error('trying to read associated crystal screen for crystal plate {0!s}'.format(barcode))
#                query = db.select([self.dbObject.crystalplateTable.columns.CrystalScreen_Name]).where(
#                    self.dbObject.crystalplateTable.columns.CrystalPlate_Barcode == barcode)
#                ResultProxy = self.dbObject.connection.execute(query)
#                crystalscreen = [x[0] for x in ResultProxy.fetchall()][0]
#
#                if len(df.at[index, 'CrystalPlate_Well']) == 2:
#                    well = df.at[index, 'CrystalPlate_Well'][0] + '0' + df.at[index, 'CrystalPlate_Well'][1]
#                else:
#                    well = df.at[index, 'CrystalPlate_Well']
#                subwell = df.at[index, 'CrystalPlate_Subwell']
#                marked_crystal_id = barcode + '-' + well + subwell
#
#                crystalscreen_id = crystalscreen + '-' + well
#
#                if marked_crystal_id not in marked_crystals:
#                    self.logger.info('marking crystal for mounting/ soaking in database: ' + marked_crystal_id)
#                    values_list = [{
#                        'MarkedCrystal_ID': marked_crystal_id,
#                        'CrystalPlate_Barcode': barcode,
#                        'CrystalPlate_Well': well,
#                        'CrystalPlate_Subwell': subwell,
#                        'CrystalScreen_ID': crystalscreen_id
#                    }]
#                    query = db.insert(self.dbObject.markedcrystalTable)
#                    self.dbObject.connection.execute(query, values_list)
#                    marked_crystals.append(marked_crystal_id)
#                else:
#                    self.logger.info('updating information for: ' + marked_crystal_id)
#
#                    query = db.update(self.dbObject.markedcrystalTable).values(
#                        CrystalScreen_ID=crystalscreen_id
#                    ).where(
#                        self.dbObject.markedcrystalTable.columns.MarkedCrystal_ID == marked_crystal_id)
#                    self.dbObject.connection.execute(query)
#                    marked_crystals.append(marked_crystal_id)
#
#            except TypeError:
#                logger.error(
#                    'there is something wrong with well and/ or subwell description: well = {0!s}, subwell = {1!s}; please correct!'.format(
#                        df.at[index, 'CrystalPlate_Well'], df.at[index, 'CrystalPlate_Subwell']))
#                continue
#
#            if Manual_Crystal_ID in existing_manually_mounted_crystals:
#                self.logger.warning('updating records for manually mounted crystal: {0!s}'.format(well))
##                self.logger.warning('updating records for manually mounted crystal: {0!s}'.format(well, condition))
#                query = db.update(self.dbObject.mountedcrystalTable).values(
#                    Pin_Barcode=df.at[index, 'Pin_Barcode'],
#                    Puck_Name=df.at[index, 'Puck_Name'],
#                    Puck_Position=str(df.at[index, 'Puck_Position']),
#                    CompoundBatch_ID=df.at[index, 'CompoundBatch_ID'],
#                    Cryo=df.at[index, 'Cryo'],
#                    Cryo_Concentration=df.at[index, 'Cryo_Concentration'],
#                    Comment=df.at[index, 'Comment'],
#                    MarkedCrystal_ID=marked_crystal_id
#                ).where(
#                    self.dbObject.mountedcrystalTable.columns.Manual_Crystal_ID == Manual_Crystal_ID)
#                self.dbObject.connection.execute(query)
#            else:
#                Crystal_ID = str(proteinacronym) + '-x' + '0' * (4 - len(str(next_crystal_number))) + str(
#                    next_crystal_number)
#                self.logger.info('inserting new records for manually mounted crystal: {0!s} as {1!s}'.format(Manual_Crystal_ID,
#                                                                                                    Crystal_ID))
#                values_list = [{
#                    'Manual_Crystal_ID': Manual_Crystal_ID,
#                    'Crystal_ID': Crystal_ID,
#                    'Pin_Barcode': df.at[index, 'Pin_Barcode'],
#                    'Puck_Name': df.at[index, 'Puck_Name'],
#                    'Puck_Position': str(df.at[index, 'Puck_Position']),
#                    'CompoundBatch_ID': df.at[index, 'CompoundBatch_ID'],
#                    'Cryo': df.at[index, 'Cryo'],
#                    'Cryo_Concentration': df.at[index, 'Cryo_Concentration'],
#                    'Comment': df.at[index, 'Comment'],
#                    'MarkedCrystal_ID': marked_crystal_id
#                }]
#                query = db.insert(self.dbObject.mountedcrystalTable)
#                self.dbObject.connection.execute(query, values_list)
#
#                next_crystal_number += 1
#
