import os
import sys

import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def read_opentrons_soak_plate_csv_file(logger, soak_plate_csv):
    logger.info('reading soak plate CSV file ' + soak_plate_csv)
    df = pd.read_csv(soak_plate_csv, dtype=str)  # set dtype otherwise 01 becomes 1
    # turn all rows that have an empty marked_crystal_code field into nan
    df['marked_crystal_code'].replace('', np.nan, inplace=True)
    # remove these fields because we are only interested in the ones that have soaked crystals
    df.dropna(subset=['marked_crystal_code'], inplace=True)
    soaked_cystal_list = df.to_dict('records')  # 'records' turns df into list of dicts
    return soaked_cystal_list

def get_unique_crystal_plate_barcodes(soaked_cystal_list):
    barcode_list = []
    for item in soaked_cystal_list:
        marked_crystal_code = item[3]
        #  d['marked_crystal_code'] = d['crystal_plate_barcode'] + '-' + d['crystal_plate_well'] + '-' + d['crystal_plate_subwell']
        barcode = marked_crystal_code.split('-')[0]
        if barcode not in barcode_list:
            barcode_list.append(barcode)
    return barcode_list

def prepare_csv(logger, folder, barcode):
    shifter_csv_file = os.path.join(folder, '3-mount', xtal_plate + '_mount.csv')
    if os.path.isfile(shifter_csv_file):
        misc.backup_file(logger, folder, barcode + '_mount.csv')
    else:
        logger.info('creating {0!s}_mount.csv file in 3-mount folder'.format(xtal_plate))
        f = open(shifter_csv_file, 'w')
        f.write('')
        f.close()
    return shifter_csv_file

def xtbm_exists(logger, shifter_csv_file, d):
    found_xtbm = False
    for line in open(shifter_csv_file, encoding='utf-8-sig'):
        ld = misc.read_line_from_shifter_csv(logger, line)
        if d['row'] == ld['PlateRow'] and d['column'] == ld['PlateColumn'] and d['subwell'] == ld['PositionSubWell']:
            logger.info('xtbm exists in file: {0!s} {1!s} {2!s'.format(d['row'], d['column'], d['subwell']))
            found_xtbm = True
            break
    return found_xtbm

def get_item_as_dict(item):
    d = {}
    marked_crystal_code = item[3]
    d['crystal_plate_barcode'] = marked_crystal_code.split('-')[0]
    crystal_plate_well = marked_crystal_code.split('-')[1]
    d['row'] = crystal_plate_well[0]
    d['column'] = str(int(crystal_plate_well[1:]))
    d['subwell'] = misc.numeric_subwell_to_letter(marked_crystal_code.split('-')[2])
    return d

def append_xtbm_to_shifter_csv(logger, shifter_csv_file, d):
    logger.info('adding xtbm to file: {0!s} {1!s} {2!s'.format(d['row'], d['column'], d['subwell']))
    f = open(shifter_csv_file, 'a')
    f.write(
        '{0!s},{1!s},AM,{2!s},{3!s},{4!s},,,,,,,,,\n'.format(plate_type, xtal_plate, row, str(int(column)), subwell))
    f.close()

def save_shifter_csv_file_for_mounting(logger, folder, soaked_cystal_list):
    logger.info('saving xtbms to ' + folder)
    barcode_list = get_unique_crystal_plate_barcodes(soaked_cystal_list)
    for barcode in barcode_list:
        logger.info('preparing {0!s}_mount.csv file'.format(barcode))
        shifter_csv_file = prepare_csv(logger, folder, barcode)
        for item in soaked_cystal_list:
            d = get_item_as_dict(item)
            if d['crystal_plate_barcode'] == barcode:
                if not xtbm_exists(logger, shifter_csv_file, d):
                    append_xtbm_to_shifter_csv(logger, shifter_csv_file, d)



