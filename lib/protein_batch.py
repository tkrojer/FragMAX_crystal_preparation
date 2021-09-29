import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from tkinter import Tk, filedialog
from IPython.display import display,clear_output
import sqlalchemy as db
import datetime

class protein_batch(object):
    def __init__(self, dbObject, logger, crystalplateObject):
        self.logger = logger

        self.dbObject = dbObject

        self.crystalplateObject = crystalplateObject

        self.last_tab = 0
        self.protein_batch_tab_list = []

        self.protein_batch_tab_dict = {}

        self.top_grid_widget = widgets.GridspecLayout(2, 3)
        self.read_batch_to_db_button = widgets.Button(description='Load Batches from DB', style= {'button_color':'orange'})
        self.top_grid_widget[0, 0] = self.read_batch_to_db_button
        self.read_batch_to_db_button.on_click(self.read_batch_to_db)

        self.add_batch_button = widgets.Button(description='Add protein batch')
        self.top_grid_widget[0, 1] = self.add_batch_button
        self.add_batch_button.on_click(self.add_batch)

        self.tab = widgets.Tab(children=[])

        self.save_batch_to_db_button = widgets.Button(description='Save to database')
        self.save_batch_to_db_button.on_click(self.save_batch_to_db)


    def add_batch(self, b):
        self.add_batch_tab(None, '', '', None, '', '', '', '')

    def add_batch_tab(self, proteinbatch, expression_host, comment, date, supplier_id, sequence, buffer, concentration):
        self.protein_batch_tab_list.append(self.add_tab_widget(proteinbatch, expression_host, comment, date, supplier_id, sequence, buffer, concentration))
        self.tab.children = self.protein_batch_tab_list
        self.tab.set_title(self.last_tab, 'batch {0!s}'.format(self.last_tab))
        self.last_tab += 1

    def get_protein_acronym(self):
        query = db.select([self.dbObject.proteinTable.columns.Protein_Acronym.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        result = ResultProxy.fetchall()
        if result:
            proteinacronym = result[0][0]
        else:
            proteinacronym = None
        return proteinacronym

    def add_tab_widget(self, proteinbatch, expr_host, com, date, sup, seq, buf, con):
        proteinacronym = self.get_protein_acronym()

        if proteinbatch == None:
            proteinbatch = str(proteinacronym) + '-b' + '0' * (2 - len(str(self.last_tab+1))) + str(self.last_tab+1)
        expression_host = widgets.Text(value=expr_host, layout=widgets.Layout(height="auto", width="200"))
        comment = widgets.Textarea(value=com, layout=widgets.Layout(height="auto", width="200"))
        date_received = widgets.DatePicker(disabled=False)
        supplier_id = widgets.Text(value=sup, layout=widgets.Layout(height="auto", width="200"))
        sequence = widgets.Textarea(value=seq, layout=widgets.Layout(height="auto", width="200"))
        buffer = widgets.Text(value=buf, layout=widgets.Layout(height="auto", width="200"))
        concentration = widgets.Text(value=con, layout=widgets.Layout(height="auto", width="200"))
        if date != None:
            date_received.value = date

        self.protein_batch_tab_dict[proteinbatch] = []

        self.protein_batch_tab_dict[proteinbatch].append(expression_host)
        self.protein_batch_tab_dict[proteinbatch].append(comment)
        self.protein_batch_tab_dict[proteinbatch].append(date_received)
        self.protein_batch_tab_dict[proteinbatch].append(supplier_id)
        self.protein_batch_tab_dict[proteinbatch].append(sequence)
        self.protein_batch_tab_dict[proteinbatch].append(buffer)
        self.protein_batch_tab_dict[proteinbatch].append(concentration)

        grid_widget = widgets.GridspecLayout(10, 4)
        grid_widget[0, 0] = Label("Batch: {0!s}".format(proteinbatch), layout=Layout(display="flex", justify_content="center"))
        grid_widget[1, 0] = Label("Supplier ID", layout=Layout(display="flex", justify_content="center"))
        grid_widget[1, 1:] = supplier_id
        grid_widget[2, 0] = Label("Buffer", layout=Layout(display="flex", justify_content="center"))
        grid_widget[2, 1:] = buffer
        grid_widget[3, 0] = Label("Concentration (mg/ml)", layout=Layout(display="flex", justify_content="center"))
        grid_widget[3, 1:] = concentration
        grid_widget[4, 0] = Label("Expression host", layout=Layout(display="flex", justify_content="center"))
        grid_widget[4, 1:] = expression_host
        grid_widget[5, 0] = Label("Sequence", layout=Layout(display="flex", justify_content="center"))
        grid_widget[5, 1:] = sequence
        grid_widget[6, 0] = Label("Comment", layout=Layout(display="flex", justify_content="center"))
        grid_widget[6, 1:] = comment
        grid_widget[7, 0] = Label("Date received", layout=Layout(display="flex", justify_content="center"))
        grid_widget[7, 1:] = date_received
        vbox = VBox(children=[grid_widget])
        return vbox

    def save_batch_to_db(self, b):
        query = db.select([self.dbObject.proteinBatchTable.columns.ProteinBatch_ID.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_batches = [x[0] for x in ResultProxy.fetchall()]

        self.logger.info('existing project batches: ' + str(existing_batches))

        for batch in self.protein_batch_tab_dict:
            expression_host = self.protein_batch_tab_dict[batch][0].value
            comment = self.protein_batch_tab_dict[batch][1].value
            date_received = self.protein_batch_tab_dict[batch][2].value
            supplier_id = self.protein_batch_tab_dict[batch][3].value
            sequence = self.protein_batch_tab_dict[batch][4].value
            buffer = self.protein_batch_tab_dict[batch][5].value
            concentration = self.protein_batch_tab_dict[batch][6].value

            if batch in existing_batches:
                self.logger.warning(
                    'protein batch  ' + batch + ' exists in database; updating records...')
                query = db.update(self.dbObject.proteinBatchTable).values(
                    Expression_Host=expression_host,
                    Comment=comment,
                    Date_received=date_received,
                    ProteinBatch_Supplier_ID=supplier_id,
                    Sequence=sequence,
                    Buffer=buffer,
                    Concentration=concentration
                ).where(self.dbObject.proteinBatchTable.columns.ProteinBatch_ID == batch)
                self.dbObject.connection.execute(query)
            else:
                self.logger.info(
                    'protein batch ' + batch + ' does not exist in database; inserting records...')
                values_list = [{
                    'ProteinBatch_ID': batch,
                    'Protein_Acronym': batch.split('-')[0],
                    'Expression_Host': expression_host,
                    'Comment': comment,
                    'Date_received': date_received,
                    'ProteinBatch_Supplier_ID': supplier_id,
                    'Sequence': sequence,
                    'Buffer': buffer,
                    'Concentration': concentration
                }]
#                query = db.insert(self.dbObject.proteinBatchTable).prefix_with("OR REPLACE")
                query = db.insert(self.dbObject.proteinBatchTable).prefix_with("OR REPLACE")
                self.dbObject.connection.execute(query, values_list)

        self.update_crystal_plate_widgets()

    def get_batches_from_db(self):
        self.logger.info('fetching existing protein batches from database...')
        query = db.select([self.dbObject.proteinBatchTable.columns.ProteinBatch_ID,
                           self.dbObject.proteinBatchTable.columns.Expression_Host,
                           self.dbObject.proteinBatchTable.columns.Comment,
                           self.dbObject.proteinBatchTable.columns.Date_received,
                           self.dbObject.proteinBatchTable.columns.ProteinBatch_Supplier_ID,
                           self.dbObject.proteinBatchTable.columns.Sequence,
                           self.dbObject.proteinBatchTable.columns.Buffer,
                           self.dbObject.proteinBatchTable.columns.Concentration]
                          ).order_by(
                           self.dbObject.proteinBatchTable.columns.ProteinBatch_ID.asc())
        ResultProxy = self.dbObject.connection.execute(query)
        result = ResultProxy.fetchall()
        return result


    def read_batch_to_db(self, b):
        result = self.get_batches_from_db()
        for b in result:
            proteinbatch = b[0]
            expression_host = b[1]
            comment = b[2]
            year = int(b[3].split('-')[0])
            month = int(b[3].split('-')[1])
            day = int(b[3].split('-')[2])
            date = datetime.date(year, month, day)
            supplier_id = b[4]
            sequence = b[5]
            buffer = b[6]
            concentration = b[7]
            if proteinbatch in self.protein_batch_tab_dict:
                self.protein_batch_tab_dict[batch][0].value = expression_host
                self.protein_batch_tab_dict[batch][1].value = comment
                self.protein_batch_tab_dict[batch][2].value = b[3]
                self.protein_batch_tab_dict[batch][3].value = b[4]
                self.protein_batch_tab_dict[batch][4].value = b[5]
                self.protein_batch_tab_dict[batch][5].value = b[6]
                self.protein_batch_tab_dict[batch][6].value = b[7]
            else:
                self.add_batch_tab(proteinbatch, expression_host, comment, date, supplier_id, sequence, buffer, concentration)


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
