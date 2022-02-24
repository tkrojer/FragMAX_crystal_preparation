import os.path

import ipywidgets as widgets
from ipywidgets import HBox, VBox, Layout, IntProgress, Label

from datetime import datetime

import sqlalchemy as db

class eln_entry(object):
    def __init__(self, settingsObject, logger, dbObject):

        self.settings = settingsObject

        self.logger = logger

        self.dbObject = dbObject

        self.last_tab = 0

        self.eln_tab_list = []
        self.eln_tab_dict = {}

        self.top_grid_widget = widgets.GridspecLayout(2, 3)
        self.read_eln_from_db_button = widgets.Button(description='Load Entries from DB',
                                                      style= {'button_color':'orange'})
        self.top_grid_widget[0, 0] = self.read_eln_from_db_button
        self.read_eln_from_db_button.on_click(self.read_eln_from_db)

        self.add_eln_entry_button = widgets.Button(description='Add Entry')
        self.top_grid_widget[0, 1] = self.add_eln_entry_button
        self.add_eln_entry_button.on_click(self.add_eln_entry)

        self.tab = widgets.Tab(children=[])

        self.save_eln_entries_to_db_button = widgets.Button(description='Save to database')
        self.save_eln_entries_to_db_button.on_click(self.save_eln_entries_to_db)

#        self.grid_widget = widgets.GridspecLayout(10, 4)
#        self.grid_widget[0,0] = Label("Title", layout=Layout(display="flex", justify_content="center"))
#
#        self.title = widgets.Text(value='', layout=widgets.Layout(height="auto", width="100"))
#
#        # data created
#        # date modified
#
#        self.comment = widgets.Textarea(value='', layout=widgets.Layout(height="auto", width="100"))
#
#        self.attachment1_label = Label("Att1", layout=Layout(display="flex", justify_content="center"))
#        self.attachment1_name = Label("Att1", layout=Layout(display="flex", justify_content="center"))
#        self.attachment1_load = widgets.Button(description='Select')
#
#        # attachments

    def add_eln_entry(self, b):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_eln('', '', str(self.last_tab), now)


    def add_eln(self, title, comment, entry_id, date_created):
        self.eln_tab_list.append(self.add_tab_widget(title, comment, entry_id, date_created))
        self.tab.children = self.eln_tab_list
        self.tab.set_title(self.last_tab, 'entry {0!s}'.format(self.last_tab))
        self.last_tab += 1

    def add_tab_widget(self, t, c, i, now):
        eln_id = i

        title = widgets.Text(value=t, layout=widgets.Layout(height="auto", width="500px"))
        comment = widgets.Textarea(value=c, layout=widgets.Layout(height="auto", width="500px"))
#        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.eln_tab_dict[eln_id] = []

        self.eln_tab_dict[eln_id].append(title)
        self.eln_tab_dict[eln_id].append(comment)
        self.eln_tab_dict[eln_id].append(now)


        grid_widget = widgets.GridspecLayout(4, 10)
        grid_widget[1, 0] = Label("Date created:", layout=Layout(display="flex", justify_content="center"))
        grid_widget[1, 1:] = Label(str(now),
                                  layout=Layout(display="flex", justify_content="center"))
        grid_widget[2, 0] = Label("Title:", layout=Layout(display="flex", justify_content="center"))
        grid_widget[2, 1:] = title
        grid_widget[3, 0] = Label("Comment:", layout=Layout(display="flex", justify_content="center"))
        grid_widget[3:10, 1:] = comment

        vbox = VBox(children=[grid_widget])
        return vbox

    def save_text_to_eln_folder(self, id, title, comment):
        if not os.path.isdir(os.path.join(self.settings.eln_folder, id)):
            os.mkdir(os.path.join(self.settings.eln_folder, id))
        if not os.path.isdir(os.path.join(self.settings.eln_folder, id, 'attachments')):
            os.mkdir(os.path.join(self.settings.eln_folder, id, 'attachments'))

        self.logger.info('saving title and comments to {0!s}'.format(os.path.join(self.settings.eln_folder, id)))

        f = open(os.path.join(self.settings.eln_folder, id, 'title.txt'), 'w')
        f.write(title)
        f.close()

        f = open(os.path.join(self.settings.eln_folder, id, 'comment.txt'), 'w')
        f.write(comment)
        f.close()

    def save_eln_entries_to_db(self, b):
        query = db.select([self.dbObject.diaryTable.columns.Entry_ID.distinct()])
        ResultProxy = self.dbObject.connection.execute(query)
        existing_entries = [x[0] for x in ResultProxy.fetchall()]

#        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for id in self.eln_tab_dict:
            title = self.eln_tab_dict[id][0].value
            comment = self.eln_tab_dict[id][1].value
            now = self.eln_tab_dict[id][2]

            if id in existing_entries:
                self.logger.warning(
                    'entry ' + id + ' exists in database; updating records...')
                query = db.update(self.dbObject.diaryTable).values(
                    EntryName=title,
                    Date_modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ).where(self.dbObject.diaryTable.columns.Entry_ID == id)
                self.dbObject.connection.execute(query)
            else:
                self.logger.info(
                    'entry ' + id + ' does not exist in database; inserting records...')
                values_list = [{
                    'Entry_ID': id,
                    'EntryName': title,
                    'Date_created': now
                }]
                query = db.insert(self.dbObject.diaryTable).prefix_with("OR REPLACE")
                self.dbObject.connection.execute(query, values_list)

            self.save_text_to_eln_folder(id, title, comment)

    def get_entries_from_db(self):
        self.logger.info('fetching existing ELN entries from database...')
        query = db.select([self.dbObject.diaryTable.columns.Entry_ID,
                           self.dbObject.diaryTable.columns.EntryName,
                           self.dbObject.diaryTable.columns.Date_created,
                           self.dbObject.diaryTable.columns.Date_modified
                          ]).order_by(
                           self.dbObject.diaryTable.columns.Entry_ID.asc())
        ResultProxy = self.dbObject.connection.execute(query)
        result = ResultProxy.fetchall()
        return result


    def read_eln_from_db(self, b):
        self.check_existing_entries_in_db()

    def check_existing_entries_in_db(self):
        result = self.get_entries_from_db()
        for b in result:
            entry_id = b[0]
            entry_name = b[1]
            date_created = b[2]
            comment = ''
            if os.path.isfile(os.path.join(self.settings.eln_folder, entry_id, 'comment.txt')):
                for line in open(os.path.join(self.settings.eln_folder, entry_id, 'comment.txt')):
                    comment += line

#            self.add_tab_widget(entry_name, comment, entry_id)
            self.add_eln(entry_name, comment, entry_id, date_created)