import os
import pandas as pd

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def column_range(start_column, end_column):
    column_range = []
    columns = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    add_column = False
    for c in columns:
        if c == start_column:
            add_column = True
        if add_column:
            column_range.append(c)
        if c == end_column:
            add_column = False
    return column_range

def row_range(start_row, end_row):
    row_range = []
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    add_row = False
    for c in rows:
        if c == start_row:
            add_row = True
        if add_row:
            row_range.append(c)
        if c == end_row:
            add_row = False
    return row_range

def subwell_range(subwell_01, subwell_02, subwell_03):
    subwell_range = []
    if int(subwell_01) != 0:
        subwell_range.append('01')
    if int(subwell_02) != 0:
        subwell_range.append('02')
    if int(subwell_03) != 0:
        subwell_range.append('03')
    return subwell_range

def save_crystal_plate_csv_to_inspect_folder(logger, subwell_01, subwell_02, subwell_03, barcode, plate_type, folder,
                                             start_row, end_row, start_column, end_column, pgbar):
    logger.info('writing crystal plate CSV file as ' + os.path.join(folder, '1-inspect', barcode + '.csv'))
    misc.backup_file(logger, os.path.join(folder, '1-inspect'), barcode + '.csv')
    start, step = misc.get_step_for_progress_bar(len(row_range(start_row, end_row)))
    data = []
    for row in row_range(start_row, end_row):
        start += step
        pgbar.value = int(start)
        for column in column_range(start_column, end_column):
            for subwell in subwell_range(subwell_01, subwell_02, subwell_03):
                data.append([plate_type, barcode, row, column, subwell, ''])
    df = pd.DataFrame(data, columns=misc.crystal_plate_header())
    df.to_csv(os.path.join(os.path.join(folder, '1-inspect', barcode + '.csv')), index=False)
    pgbar.value = 0
    logger.info('finished writing crystal plate CSV file as ' + os.path.join(folder, '1-inspect', barcode + '.csv'))