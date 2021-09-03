import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
import misc
import pandas as pd
import qgrid

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
#        self.add_screen_button.on_click(add_screen)
        self.grid_widget[0, 2] = self.add_screen_button
        self.grid_widget[1, 0] = Label("Select Screen", layout=Layout(display="flex", justify_content="center"))
        self.select_screen = widgets.Dropdown()
        self.grid_widget[1, 1] = self.select_screen

        self.refresh_screen_button = widgets.Button(description='Refresh Screen List',
                                               tooltip=misc.refresh_screen_button_tip())
#        self.refresh_screen_button.on_click(self.refresh_screen_dropdown)
        self.grid_widget[1, 2] = self.refresh_screen_button

        self.load_selected_screen_button = widgets.Button(description="Load Screen from DB",
                                                     layout=widgets.Layout(height="auto", width="auto"),
                                                     tooltip=misc.load_selected_screen_button_tip())
#        self.load_selected_screen_button.on_click(self.load_screen_from_db)
        self.grid_widget[2, 0] = self.load_selected_screen_button

        self.save_screen_csv_button = widgets.Button(description="Save CSV template",
                                                layout=widgets.Layout(height="auto", width="auto"),
                                                tooltip=misc.save_screen_csv_button_tip(str(self.settings.crystal_screen_folder),
                                                                                        str(self.select_screen.value)))
#        self.save_screen_csv_button.on_click(self.save_screen_csv)
        self.grid_widget[2, 1] = self.save_screen_csv_button

        self.upload_screen_csv_button = widgets.Button(description="Upload CSV file",
                                                  layout=widgets.Layout(height="auto", width="auto"))
#        self.upload_screen_csv_button.on_click(self.upload_screen_csv)
        self.grid_widget[2, 2] = self.upload_screen_csv_button

        self.import_dragonfly_button = widgets.Button(description="Import Dragonfly file",
                                                 layout=widgets.Layout(height="auto", width="auto"))
#        self.import_dragonfly_button.on_click(self.import_dragonfly)
        self.grid_widget[2, 3] = self.import_dragonfly_button

        #
        # ipysheet
        #

        # screen_sheet = sheet(rows=96, columns=2, column_headers=['CrystalScreen_Well','CrystalScreen_Condition'])
        # screen_sheet.layout.height = '350px'   # adjust to monitor size
#        df_template = pd.read_csv(self.crystal_plate_template)
        # screen_sheet = qgrid.show_grid(df, grid_options={'sortable': False})
        # grid_options={'forceFitColumns': False, 'defaultColumnWidth': 100}
#        self.screen_sheet = qgrid.QgridWidget(df=df_template, show_toolbar=False)

#        self.save_screen_to_db_button = widgets.Button(description='Save CrystalScreen to Database',
#                                                  layout=widgets.Layout(height="auto", width="auto"),
#                                                  style={'button_color': 'gray'})
#        self.save_screen_to_db_button.on_click(self.save_screen_to_db)

#        self.crystal_screen_progress = IntProgress(min=0, max=95)
