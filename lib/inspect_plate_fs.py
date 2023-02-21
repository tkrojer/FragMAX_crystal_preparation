import os
import pandas as pd

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def get_crystal_drop_list_from_csv(logger, barcode, folder):
    logger.info('trying to get crystal droplet info for {0!s}.csv in {1!s}'.format(barcode, folder))
    d = None
    if os.path.isfile(os.path.join(folder, barcode + '.csv')):
        df = pd.read_csv(os.path.join(folder, barcode + '.csv'), dtype = str) # set dtype otherwise 01 becomes 1
        d = df.to_dict('records')   # 'records' turns df into list of dicts
    else:
        logger.error('file {0!s}.csv does not exist in {1!s}'.format(barcode, folder))
    return d

def read_crystal_image_list(logger, barcode, folder, inspect_folder):
    logger.info('trying to read crystal images for plate {0!s} in {1!s}'.format(barcode, folder))
    drop_list = get_crystal_drop_list_from_csv(logger, barcode, inspect_folder)
    l = []
    for i in sorted(glob.glob(os.path.join(folder, '*.jpg'))):
        fn = os.path.basename(i)
        if barcode in fn:
            if fn.split('_')[13] == '00':
                column, row, subwell = misc.get_row_column_subwell_from_filename(i)
#                logger.warning('--- {0!s} {1!s} {2!s}'.format(column, row, subwell))
                row_letter = misc.get_row_letter_from_row_number(row, misc.swiss_ci_3_drop_layout())
#                logger.warning('=== {0!s}'.format(row_letter))
                if crystallization_drop_exists(drop_list, row_letter, column, subwell):
                    l.append(i)
                else:
                    logger.warning('no entry for {0!s} {1!s} {2!s} in {3!s}.csv'.format(
                        column_letter, row, subwell, barcode))
    logger.info('found {0!s} crystal images'.format(len(l)))
    return l

def crystallization_drop_exists(drop_list, row, column, subwell):
    drop_exists = False
    for item in drop_list:
        r = item['crystal_plate_row']
        c = item['crystal_plate_column']
        s = item['crystal_plate_subwell']
        if row == r and column == c and subwell == s:
            drop_exists = True
            break
    return drop_exists

def check_for_marked_crystals(logger, barcode, folder):
    marked_crystal_list = []
    csv_file = os.path.join(folder, '2-soak', barcode + '_xtal.csv')
    logger.info('checking for marked/ soaked crystals in ' + csv_file)
    if os.path.isfile(csv_file):
        logger.info('file exists')
        # plate_type, barcode, row_letter, column, subwell, status
        df = pd.read_csv(os.path.join(csv_file), dtype=str)
        # if you want to remove columns in dataframe df.drop(columns=["Letter", "GDP per capita"])
#        df['status'] = 'old'
        marked_crystal_list = df.values.tolist()
    return marked_crystal_list

def save_crystal_plate_csv_to_soak_folder(logger, marked_crystal_list, barcode, folder, plate_type):
    logger.info('writing marked crystal CSV file as ' + os.path.join(folder, '2-soak', barcode + '_xtal.csv'))
    misc.backup_file(logger, os.path.join(folder, '2-soak'), barcode + '_xtal.csv')
    data = []
    if os.path.isfile(os.path.join(folder, '2-soak', barcode + '_xtal.csv')):
        logger.warning('file exists ' + os.path.join(folder, '2-soak', barcode + '_xtal.csv'))
        logger.info('will read in existing records and add new ones')
        df = pd.read_csv(os.path.join(folder, '2-soak', barcode + '_xtal.csv'), dtype = str)
        data = df.values.tolist()
    for item in marked_crystal_list:
        plate_type = item[0]
        barcode = item[1]
        row_letter = item[2]
        column = item[3]
        subwell = item[4]
        status = item[5]
        if status == 'new':
            logger.info('adding new marked crystal to {0!s}.csv: row {1!s} - col {2!s} - sub {3!s}'.format(
                barcode, row_letter, column, subwell))
            data.append([plate_type, barcode, row_letter, column, subwell, 'marked'])
        else:
            logger.warning('skipping row {0!s} - col {1!s} - sub {2!s}; status: {3!s}'.format(
                row_letter, column, subwell, status))
    if data:
        df = pd.DataFrame(data, columns=misc.crystal_plate_header())
        df.to_csv(os.path.join(os.path.join(folder, '2-soak', barcode + '_xtal.csv')), index=False)
    else:
        logger.warning('looks like there were no new crystals marked for plate ' + barcode)
