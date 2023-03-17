import ipywidgets as widgets
import os

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import soak_plate_fs as fs
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query
import soak_plate_db as db

class soak_plate_tab(object):
    def __init__(self, settingsObject, dal, logger, pgbar):

        self.settingsObject = settingsObject
        self.dal = dal
        self.logger = logger
        self.pgbar = pgbar

        self.grid_widget = widgets.GridspecLayout(10, 4)

        self.grid_widget[0, 0] = widgets.Button(description="Enter New Soak Plate Name",
                           layout=widgets.Layout(width="auto"), style= {'button_color':'white'})
        self.soakplate_name = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget[0, 1] = self.soakplate_name
        add_soakplate_name_button = widgets.Button(description='Add')
        add_soakplate_name_button.on_click(self.add_soakplate)
        self.grid_widget[0, 2] = add_soakplate_name_button

        self.grid_widget[1, 0] = widgets.Button(description="Select Soak Plate",
                           layout=widgets.Layout(width="auto"), style= {'button_color': 'white'})
        self.select_soakplate = widgets.Dropdown()
        self.grid_widget[1, 1] = self.select_soakplate
        refresh_soakplate_button = widgets.Button(description='Refresh Soak Plate List')
        refresh_soakplate_button.on_click(self.refresh_soakplate)
        self.grid_widget[1, 2] = refresh_soakplate_button

        self.grid_widget[2, 0] = widgets.Button(description="Select Library Plate",
                           layout=widgets.Layout(width="auto"), style= {'button_color': 'white'})
        self.select_library_plate = widgets.Dropdown()
        self.grid_widget[2, 1] = self.select_library_plate
        refresh_library_plate_button = widgets.Button(description='Refresh Library Plate List')
        refresh_library_plate_button.on_click(self.refresh_libraryplate)
        self.grid_widget[2, 2] = refresh_library_plate_button

        self.grid_widget[3, 0] = widgets.Button(description="Reservoir Condition",
                           layout=widgets.Layout(width="auto"), style= {'button_color': 'white'})
        self.soakplate_reservoir = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget[3, 1:] = self.soakplate_reservoir

        self.grid_widget[4, 0] = widgets.Button(description="Reservoir Volume (\u03BCL)",
                           layout=widgets.Layout(width="auto"), style= {'button_color': 'white'})
        self.soakplate_reservoir_volume = widgets.Text(value='', layout=widgets.Layout(width="200"))
        self.grid_widget[4, 1:] = self.soakplate_reservoir_volume

        self.grid_widget[5, 0] = widgets.Button(description="Compound Volume (\u03BCL)",
                           layout=widgets.Layout(width="auto"), style= {'button_color': 'white'})
        self.soakplate_compound_volume = widgets.Text(value='', layout=widgets.Layout(width="auto"))
        self.grid_widget[5, 1] = self.soakplate_compound_volume


        self.grid_widget[6, 0] = widgets.Button(description="Select Plate Type",
                           layout=widgets.Layout(width="auto"), style= {'button_color': 'white'})
        self.select_plate_type = widgets.Dropdown()
        self.grid_widget[6, 1] = self.select_plate_type

        save_soakplate_button = widgets.Button(description='Save Soak Plate to DB & CSV',
                                               layout=widgets.Layout(width="auto"), style= {'button_color': 'orange'})
        save_soakplate_button.on_click(self.save_soakplate_to_db)
        self.grid_widget[7, 0:] = save_soakplate_button

    def add_soakplate(self, b):
        l = []
        for opt in self.select_soakplate.options: l.append(opt)
        if self.soakplate_name.value not in l:
            self.logger.info('adding ' + self.soakplate_name.value + ' to soakplate dropdown')
            l.append(self.soakplate_name.value)
        else:
            self.logger.warning(self.soakplate_name.value + ' exists in soakplate dropdown')
        self.select_soakplate.options = l

    def refresh_soakplate(self, b):
        existing_soakplates = query.get_soak_plates_for_dropdown(self.dal, self.logger)
        self.select_soakplate.options = existing_soakplates

    def refresh_libraryplate(self, b):
        existing_compoundplates = query.get_compound_plates_for_dropdown(self.dal, self.logger)
        self.select_library_plate.options = existing_compoundplates

    def save_soakplate_to_db(self, b):
        d = {}
        d['soak_plate_name'] = self.select_soakplate.value
        d['base_buffer'] = self.soakplate_reservoir.value
        d['compound_plate_name'] = self.select_library_plate.value
        d['soak_plate_type'] = self.select_plate_type.value

        try:
            d['base_buffer_volume'] = float(self.soakplate_reservoir_volume.value)
        except ValueError:
            d['base_buffer_volume'] = 0.0
        d['base_buffer_volume_unit'] = 'uL'

        try:
            d['compound_volume'] = float(self.soakplate_compound_volume.value)
        except ValueError:
            d['compound_volume'] = 0.0
        d['compound_volume_unit'] = 'uL'

        db.save_soak_plate_to_database(self.logger, self.dal, d, self.pgbar)
        self.save_soakplate_csv_file()

    def save_soakplate_csv_file(self):
        df = db.get_soak_plate_from_database_as_df(self.logger, self.dal, self.select_soakplate.value)
        fs.save_soak_plate_csv_file(self.logger, self.settingsObject.workflow_folder, self.select_soakplate.value, df)



