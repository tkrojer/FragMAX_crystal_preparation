import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label
from IPython.display import display,clear_output
from tkinter import Tk, filedialog
import os
import ntpath

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import inspect_plate_fs as fs
import misc
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query
import inspect_plate_db as db

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.lines import Line2D

class inspect_plate_tab(object):
    def __init__(self, settingsObject, dal, logger, pgbar):
        self.logger = logger
        self.dal = dal
        self.settingsObject = settingsObject
        self.pgbar = pgbar

        self.image_list = []
        self.image_number = 0
        self.marked_crystal_list = []

        self.grid_widget = widgets.GridspecLayout(9, 4, height='700px')

#        import_shifter_marked_crystals_button = widgets.Button(description='import marked crystals from shifter',
#                                                               layout=Layout(border='1px solid', width='75%'))
#        import_shifter_marked_crystals_button.on_click(self.import_shifter_marked_crystals)
#        self.grid_widget[0, :2] = import_shifter_marked_crystals_button

        self.grid_widget[1, 0] = Label("Crystal plate", layout=Layout(justify_content="center", width='100%'))
        self.select_crystal_plate = widgets.Dropdown(layout=Layout(width='100%'))
        self.grid_widget[1, 1] = self.select_crystal_plate
        load_crystal_plate_button = widgets.Button(description='Load crystal plate\nfrom database')
        load_crystal_plate_button.on_click(self.load_crystal_plate)
        self.grid_widget[1, 2] = load_crystal_plate_button
        load_crystal_image_button = widgets.Button(description='Load crystal images', style= {'button_color': 'orange'})
        load_crystal_image_button.on_click(self.load_crystal_images)
        self.grid_widget[1, 3] = load_crystal_image_button

        self.cystal_image_box = widgets.VBox(children=[], layout=Layout(border='3px solid red', width='100%'))
        self.grid_widget[2:6, 0:2] = self.cystal_image_box

        self.cystal_plate_box = widgets.VBox(children=[], layout=Layout(border='solid', width='100%'))
        self.grid_widget[2:6, 2:] = self.cystal_plate_box

        self.show_marked_crystals(None)

        prev_image_button = widgets.Button(description='<<<', layout=Layout(border='1px solid', width='100%'))
        prev_image_button.on_click(self.change_prev_crystal_image)
        self.grid_widget[6, 0] = prev_image_button
        next_image_button = widgets.Button(description='>>>', layout=Layout(border='1px solid', width='100%'))
        next_image_button.on_click(self.change_next_crystal_image)
        self.grid_widget[6, 1] = next_image_button

        mount_crystal_button = widgets.Button(description='Mount', style={'button_color': 'green'},
                                              layout=Layout(border='1px solid', width='100%'))
        mount_crystal_button.on_click(self.flag_crystal_for_mounting)
        self.grid_widget[7, 0] = mount_crystal_button
        unmount_crystal_button = widgets.Button(description='Unmount', style={'button_color': 'red'},
                                                layout=Layout(border='1px solid', width='100%'))
        unmount_crystal_button.on_click(self.unflag_crystal_for_mounting)
        self.grid_widget[7, 1] = unmount_crystal_button

        save_marked_crystals_button = widgets.Button(description='Save to DB & CSV', style={'button_color': 'orange'},
                                              layout=Layout(border='1px solid', width='100%'))
        save_marked_crystals_button.on_click(self.save_marked_crystals)
        self.grid_widget[8, 0:] = save_marked_crystals_button


    def droplet_newly_flagged(self, ro, co, su):
        exists = False
        for i in self.marked_crystal_list:
            if ro == i[2] and co == i[3] and su == i[4] and i[6] == 'new':
                exists = True
        return exists

    def droplet_already_flagged(self, ro, co, su):
        exists = False
        for i in self.marked_crystal_list:
            if ro == i[2] and co == i[3] and su == i[4] and i[6] == 'marked':
                exists = True
        return exists

    def droplet_was_soaked(self, ro, co, su):
        exists = False
        for i in self.marked_crystal_list:
            if ro == i[2] and co == i[3] and su == i[4] and i[6] == 'soaked':
                exists = True
        return exists

    def droplet_status(self, ro, co, su):
        new = self.droplet_newly_flagged(ro, co, su)
        old = self.droplet_already_flagged(ro, co, su)
        soaked = self.droplet_was_soaked(ro, co, su)
        return new, old, soaked

    def show_marked_crystals(self, crystal_image):
        cx, cy = misc.get_coordinates_from_filename(crystal_image, misc.swiss_ci_3_drop_layout())
        magnify = 2
        out = widgets.Output()
        fig, ax = plt.subplots()
        plt.xlim(0,36 * magnify)
        plt.ylim(0,25 * magnify)
        ax.set_aspect(1)
        for c in misc.swiss_ci_3_drop_layout():
            ox = c[1]
            oy = c[2]
            x = c[1] * magnify
            y = c[2] * magnify
            radius = 0.2 * magnify
            new, old, soaked = self.droplet_status(c[4], c[6], c[7])
            if c[3] == 'circle' and ox == cx and oy == cy and not (new or old or soaked):
                ax.add_artist(plt.Circle((x, y), radius * 2, color='orange'))
            elif c[3] == 'circle' and ox == cx and oy == cy and (new or old):
                ax.add_artist(plt.Circle((x, y), radius * 2, facecolor='green', edgecolor="orange", linewidth=3))
            elif c[3] == 'circle' and ox == cx and oy == cy and soaked:
                ax.add_artist(plt.Circle((x, y), radius * 2, facecolor='cyan', edgecolor="orange", linewidth=3))
            elif c[3] == 'circle' and (new or old):
                ax.add_artist(plt.Circle((x, y), radius * 1.5, color='green'))
            elif c[3] == 'circle' and soaked:
                ax.add_artist(plt.Circle((x, y), radius * 1.5, color='cyan'))
            elif c[3] == 'circle':
                ax.add_artist(plt.Circle((x, y), radius, color='gray'))
            elif c[3] == 'rectangle':
                ax.add_patch(plt.Rectangle((x-radius, y-radius), radius*2, radius*2,
                                           edgecolor='black', facecolor='none', lw=0.2))
#        fig.set_edgecolor('black')
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='current', markerfacecolor='orange', markersize=7),
            Line2D([0], [0], marker='o', color='w', label='marked', markerfacecolor='green', markersize=7),
            Line2D([0], [0], marker='o', color='w', label='soaked', markerfacecolor='cyan', markersize=7)]

#        ax.legend(handles=legend_elements, loc='lower center')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc="center",
                bbox_transform=fig.transFigure, ncol=4, handles=legend_elements)

        plt.axis("off")
        with out:
            clear_output(wait=True)
            display(plt.show())
        self.cystal_plate_box.children = [out]

    def load_crystal_plate(self, b):
        existing_crystalplates = query.get_existing_crystal_plate_barcodes(self.dal, self.logger)
        self.select_crystal_plate.options = existing_crystalplates
        self.logger.info('updating barcode selection dropdown: ' + str(existing_crystalplates))

    def load_crystal_images(self, b):
        self.image_list = fs.read_crystal_image_list(self.logger,
                                                     self.select_crystal_plate.label,
                                                     self.settingsObject.crystal_image_folder,
                                                     os.path.join(self.settingsObject.workflow_folder, '1-inspect'),
                                                     self.pgbar)
        if self.image_list:
            self.logger.info('resetting marked_crystal_list and image_number...')
            self.marked_crystal_list = fs.check_for_marked_crystals(self.logger,
                                                                    self.select_crystal_plate.label,
                                                                    self.settingsObject.workflow_folder)
            self.image_number = 0
            self.show_crystal_image()
        else:
            self.logger.error('could not find any crystal images for {0!s}'.format(self.select_crystal_plate.label))

    def flag_crystal_for_mounting(self, b):
        crystal_image = self.image_list[self.image_number]
        column, row_letter, subwell, well = misc.get_row_letter_column_subwell_well_from_filename(crystal_image)
        barcode = self.select_crystal_plate.label
        if ["SwissCI-MRC-3d", barcode, row_letter, column, subwell, 'new'] not in self.marked_crystal_list:
            # plate_type, barcode, row_letter, column, subwell, status
            self.marked_crystal_list.append(["SwissCI-MRC-3d", barcode, row_letter, column, subwell, well, 'new', '', ''])
        self.change_crystal_image(1)

    def unflag_crystal_for_mounting(self, b):
        crystal_image = self.image_list[self.image_number]
        column, row_letter, subwell, well = misc.get_row_letter_column_subwell_well_from_filename(crystal_image)
        barcode = self.select_crystal_plate.label
        if ["SwissCI-MRC-3d", barcode, row_letter, column, subwell, 'new'] in self.marked_crystal_list:
            self.marked_crystal_list.remove(["SwissCI-MRC-3d", barcode, row_letter, column, subwell, well, 'new', '', ''])
        self.change_crystal_image(1)

    def show_crystal_image(self):
        out = widgets.Output()
        crystal_image = self.image_list[self.image_number]
        with cbook.get_sample_data(crystal_image) as image_file:
            image = plt.imread(image_file)
        plt.imshow(image)
        plt.axis("off")
        column, row_letter, subwell, well = misc.get_row_letter_column_subwell_well_from_filename(crystal_image)
        plt.title('row: {0!s} - column: {1!s} - subwell: {2!s}'.format(row_letter, column, subwell))
        with out:
            clear_output(wait=True)
            display(plt.show())
        self.cystal_image_box.children = [out]
        self.show_marked_crystals(crystal_image)

    def change_crystal_image(self, n):
        self.image_number += n
        if self.image_number > len(self.image_list):
            self.image_number = len(self.image_list)
        if self.image_number < 0:
            self.image_number = 0
        self.show_crystal_image()

    def change_next_crystal_image(self, b):
        self.change_crystal_image(1)

    def change_prev_crystal_image(self, b):
        self.change_crystal_image(-1)

    def save_marked_crystals(self, b):
        """
        plate_type is hardcoded for now but will be replaced with db quiery
        """
        fs.save_crystal_plate_csv_to_soak_folder(self.logger,
                                                 self.marked_crystal_list,
                                                 self.select_crystal_plate.label,
                                                 self.settingsObject.workflow_folder,
                                                 "SwissCI-MRC-3d",
                                                 self.pgbar)
        xtal_list = misc.get_list_of_dict_from_marked_crystal_list(self.marked_crystal_list,
                                                                   self.select_crystal_plate.label)
        db.save_marked_crystals_to_db(self.dal, self.logger, xtal_list, self.pgbar, self.select_crystal_plate.value)





#    def import_shifter_marked_crystals(self, b):
#        clear_output()
#        root = Tk()
#        root.withdraw()
#        root.call('wm', 'attributes', '.', '-topmost', True)
#        b.files = filedialog.askopenfilename(multiple=True,
#                                             initialdir=os.path.join(self.settingsObject.workflow_folder, '1-inspect'),
#                                             title="Select file",
#                                             filetypes=[("CSV Files",
#                                                         ".csv")])
#        shiftercsv = b.files[0]
#        if os.path.isfile(shiftercsv):
#            if not shiftercsv.endswith('_shifter_inspect.csv'):
#                self.logger.error('selected filename is {0!s}, but file needs to end with _inspect.csv'.format(shiftercsv))
#            else:
#                xtal_list = fs.import_marked_crystals_from_shifter_csv(self.logger, shiftercsv)
##                self.update_inspected_wells_sheet(xtal_list)
#                query.save_marked_crystals_to_db(self.dal, self.logger, xtal_list)
#                folder = self.settingsObject.workflow_folder
#                fs.save_marked_crystals_to_soak_folder_as_shifter_csv(self.logger, shiftercsv, folder)
#        else:
#            self.logger.error('cannot read file ' + b.files[0])


#    def update_inspected_wells_sheet(self, xtal_list):
#        self.logger.info('updating inspected_wells_sheet widget')
#        n = 0
#        data = []
#        for xtal in xtal_list:
#            data.append([xtal['crystal_plate_barcode'], xtal['crystal_plate_well'], xtal['crystal_plate_subwell']])
#            n += 1
#        self.inspected_wells_sheet.sendModel()
#        if n < self.n_rows_inspected_wells:
#            for i in range(n, self.n_rows_inspected_wells):
#                data.append(["............", "............", "............"])
#        self.inspected_wells_sheet.sendModel()


#
# code for table
#
#        self.n_rows_inspected_wells = 288
#
#        sheet_header = [
#            'crystal_plate_barcode',
#            'crystal_plate_well',
#            'crystal_plate_subwell'
#        ]
#
#        data = []
#        for i in range(self.n_rows_inspected_wells):
#            row = []
#            for j in range(len(sheet_header)):
#                row.append("............")
#            data.append(row)
#        df = pd.DataFrame(data, columns=[sheet_header])
#
#        out = widgets.Output()
#        self.inspected_wells_sheet = pn.widgets.Tabulator(df)
#        table_box = widgets.VBox()
#        with out:
#            clear_output(wait=True)
#            display(self.inspected_wells_sheet)
#        table_box.children = [out]
