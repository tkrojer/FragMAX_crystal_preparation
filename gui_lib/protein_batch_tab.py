import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from tkinter import Tk, filedialog
from IPython.display import display,clear_output
import datetime

import os, sys
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import protein_batch_db as db
import query


class protein_batch_tab(object):
    def __init__(self, dal, logger, crystalplateObject):
        self.logger = logger
        self.dal = dal
        self.crystalplateObject = crystalplateObject

        self.last_tab = 1
        self.protein_batch_tab_list = []
        self.protein_batch_tab_dict = {}

        self.top_grid_widget = widgets.GridspecLayout(2, 3)
        self.read_batch_from_db_button = widgets.Button(description='Load Batches from DB',
                                                        style= {'button_color':'orange'})
        self.top_grid_widget[0, 0] = self.read_batch_from_db_button
        self.read_batch_from_db_button.on_click(self.read_batch_from_db)

        self.add_batch_button = widgets.Button(description='Add protein batch')
        self.top_grid_widget[0, 1] = self.add_batch_button
        self.add_batch_button.on_click(self.add_batch)

        self.tab = widgets.Tab(children=[])

        self.save_batch_to_db_button = widgets.Button(description='Save to database')
        self.save_batch_to_db_button.on_click(self.save_batch_to_db)


    def add_batch(self, b):
        self.logger.info('checking if protein batch(es) exist in database...')
        self.check_existing_batch_in_db()
        qr = {
            'protein_batch_id': None,
            'protein_batch_expression_host': '',
            'protein_batch_comment': '',
            'date_received': '',
            'protein_batch_supplier_name': '',
            'protein_batch_sequence': '',
            'protein_batch_buffer': '',
            'protein_batch_concentration': '',
            'protein_batch_concentration_unit': 'mg/ml',
            'protein_batch_date_received': None
        }
        self.add_batch_tab(qr)

    def add_batch_tab(self, qr):
        self.logger.info('creating new tab...')
        self.protein_batch_tab_list.append(self.add_tab_widget(qr))
        self.tab.children = self.protein_batch_tab_list
        self.tab.set_title(self.last_tab, 'batch {0!s}'.format(self.last_tab))
        self.last_tab += 1

    def add_tab_widget(self, qr):
        if qr['protein_batch_id'] == None:
            proteinbatch = self.last_tab
        else:
            proteinbatch = qr['protein_batch_id']
        self.logger.info('adding tab for batch {0!s}'.format(proteinbatch))

        expression_host = widgets.Text(value=qr['protein_batch_expression_host'],
                                       layout=widgets.Layout(height="auto", width="200"))
        comment = widgets.Textarea(value=qr['protein_batch_comment'],
                                   layout=widgets.Layout(height="auto", width="200"))
        date_received = widgets.DatePicker(disabled=False)
        supplier_id = widgets.Text(value=qr['protein_batch_supplier_name'],
                                   layout=widgets.Layout(height="auto", width="200"))
        sequence = widgets.Textarea(value=qr['protein_batch_sequence'],
                                    layout=widgets.Layout(height="auto", width="200"))
        buffer = widgets.Text(value=qr['protein_batch_buffer'],
                              layout=widgets.Layout(height="auto", width="200"))
        concentration = widgets.Text(value=str(qr['protein_batch_concentration']),
                                     layout=widgets.Layout(height="auto", width="200"))
        if qr['protein_batch_date_received'] is not None:
            try:
                date_received.value = qr['protein_batch_date_received']
            except AttributeError:
                self.logger.warning('protein_batch_date_received not specified')

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

    def get_protein_batch_name(self, batch):
        proteinacronym = query.get_protein_acronym(self.dal, self.logger)
        protein_batch_name = proteinacronym + '-b' + ((3-len(str(batch))) * '0') + str(batch)
        return protein_batch_name

    def save_batch_to_db(self, b):
        self.logger.info('saving batch information to database')
        l = []
        for batch in self.protein_batch_tab_dict:
            d = {
                'protein_batch_name': self.get_protein_batch_name(batch),
                'protein_batch_expression_host': self.protein_batch_tab_dict[batch][0].value,
                'protein_batch_comment': self.protein_batch_tab_dict[batch][1].value,
                'protein_batch_date_received': self.protein_batch_tab_dict[batch][2].value,
                'protein_batch_supplier_name': self.protein_batch_tab_dict[batch][3].value,
                'protein_batch_sequence': self.protein_batch_tab_dict[batch][4].value,
                'protein_batch_buffer': self.protein_batch_tab_dict[batch][5].value,
                'protein_batch_concentration': self.protein_batch_tab_dict[batch][6].value,
                'protein_batch_concentration_unit_id': 14
            }
            self.logger.info('data for protein batch: {0!s}'.format(d))
            l.append(d)
        db.save_protein_batch_to_db(self.dal, self.logger, l)
        self.update_crystal_plate_widgets()

    def read_batch_from_db(self, b):
        self.check_existing_batch_in_db()

    def check_existing_batch_in_db(self):
        result_list = db.get_protein_batches_from_db(self.dal, self.logger)
        for qr in result_list:
            proteinbatch = qr['protein_batch_id']
            if proteinbatch not in self.protein_batch_tab_dict:
                self.add_batch_tab(qr)

    def update_crystal_plate_widgets(self):
        existing_protein_batches = query.get_protein_batch_for_dropdown(self.dal, self.logger)
        self.logger.info('found the following protein batches in database: ' + str(existing_protein_batches))
        self.crystalplateObject.select_protein_batch.options = existing_protein_batches

#        query = db.select([self.dbObject.proteinBatchTable.columns.ProteinBatch_ID.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        existing_protein_batches = [x[0] for x in ResultProxy.fetchall()]
#        self.logger.info('found the following protein batches in database: ' + str(existing_protein_batches))
#        self.crystalplateObject.select_protein_batch.options = existing_protein_batches
#
#        query = db.select([self.dbObject.crystal_plate_typeTable.columns.Plate_Name.distinct()])
#        ResultProxy = self.dbObject.connection.execute(query)
#        existing_plate_types = [x[0] for x in ResultProxy.fetchall()]
#        self.logger.info('found the following crystal plate types in database: ' + str(existing_plate_types))
#        self.crystalplateObject.select_plate_type.options = existing_plate_types
