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
#    # remove these fields because we are only interested in the ones that have soaked crystals
#    df.dropna(subset=['marked_crystal_code'], inplace=True)
    # only keep the ones where status is prepared
    df = df.loc[df['status'] == 'prepared']
    soaked_cystal_list = df.to_dict('records')  # 'records' turns df into list of dicts
    return soaked_cystal_list

def read_modified_opentrons_xtal_plate_csv_file(logger, xtal_plate_csv):
    logger.info('reading crystal plate CSV file ' + xtal_plate_csv)
    df = pd.read_csv(xtal_plate_csv, dtype=str)  # set dtype otherwise 01 becomes 1
#    df.loc[df["crystal_plate_subwell"] == "01", "crystal_plate_subwell"] = "a"
#    df.loc[df["crystal_plate_subwell"] == "02", "crystal_plate_subwell"] = "c"
#    df.loc[df["crystal_plate_subwell"] == "03", "crystal_plate_subwell"] = "d"

#    df['marked_crystal_code'].replace('', np.nan, inplace=True)
    df['marked_crystal_code'] = df.apply(lambda x: "{0!s}-{1!s}-{2!s}-{3!s}".format(x['crystal_plate_barcode'],
                                                                                    x['crystal_plate_row'],
                                                                                    x['crystal_plate_column'],
                                                                                    x['crystal_plate_subwell']), axis=1)
    df = df.loc[df['status'] == 'transferred']
    df = df.drop('crystal_plate_well', axis=1)
    df = df.drop('crystal_plate_column', axis=1)
    df = df.drop('crystal_plate_barcode', axis=1)
    df = df.drop('crystal_plate_subwell', axis=1)
    df = df.drop('plate_type_name', axis=1)
    df = df.drop('crystal_plate_row', axis=1)
    soaked_cystal_list = df.to_dict('records')
    return soaked_cystal_list

def get_unique_crystal_plate_barcodes(soaked_cystal_list):
    barcode_list = []
    for d in soaked_cystal_list:
        marked_crystal_code = d['marked_crystal_code']
        #  d['marked_crystal_code'] = d['crystal_plate_barcode'] + '-' + d['crystal_plate_well'] + '-' + d['crystal_plate_subwell']
        barcode = marked_crystal_code.split('-')[0]
        if barcode not in barcode_list:
            barcode_list.append(barcode)
    return barcode_list

def prepare_csv(logger, folder, barcode):
    shifter_csv_file = os.path.join(folder, barcode + '_mount.csv')
    if os.path.isfile(shifter_csv_file):
        misc.backup_file(logger, folder, barcode + '_mount.csv')
    else:
        logger.info('creating {0!s}_mount.csv file in 3-mount folder'.format(barcode))
        f = open(shifter_csv_file, 'w')
        f.write('')
        f.close()
    return shifter_csv_file

def xtbm_exists(logger, shifter_csv_file, d):
    found_xtbm = False
    for line in open(shifter_csv_file, encoding='utf-8-sig'):
        ld = misc.read_line_from_shifter_csv(logger, line)
        print(line.split(','))
        if ld:
            if d['row'] == ld['PlateRow'] and d['column'] == ld['PlateColumn'] and d['subwell'] == ld['PositionSubWell']:
                logger.info('xtbm exists in file: {0!s} {1!s} {2!s}'.format(d['row'], d['column'], d['subwell']))
                found_xtbm = True
                break
    return found_xtbm

def get_item_as_dict(dic):
    d = {}
    marked_crystal_code = dic['marked_crystal_code']
    d['crystal_plate_barcode'] = marked_crystal_code.split('-')[0]
#    crystal_plate_well = marked_crystal_code.split('-')[1]
    d['row'] = marked_crystal_code.split('-')[1]
    d['column'] = str(int(marked_crystal_code.split('-')[2]))
    d['subwell'] = misc.numeric_subwell_to_letter(marked_crystal_code.split('-')[3])
    crystal_plate_well = d['row'] + d['column']
    return d

def append_xtbm_to_shifter_csv(logger, shifter_csv_file, d):
    logger.info('adding xtbm to file: {0!s} {1!s} {2!s}'.format(d['row'], d['column'], d['subwell']))
    f = open(shifter_csv_file, 'a')
    # plate_type is hardcoded for now; information is in crystal plate
    if d['subwell'] == '01':
        subwell = 'a'
    elif d['subwell'] == '02':
        subwell = 'c'
    elif d['subwell'] == '03':
        subwell = 'd'
    else:
        subwell = ''
    f.write(
        '{0!s},{1!s},AM,{2!s},{3!s},{4!s},,,,,,,,,\n'.format('SwissCI-MRC-3d',
                                                             d['crystal_plate_barcode'],
                                                             d['row'], d['column'], subwell))
    f.close()

def save_shifter_csv_file_for_mounting(logger, folder, soaked_cystal_list):
    logger.info('saving xtbms to ' + folder)
    barcode_list = get_unique_crystal_plate_barcodes(soaked_cystal_list)
    for barcode in barcode_list:
        logger.info('preparing {0!s}_mount.csv file'.format(barcode))
        shifter_csv_file = prepare_csv(logger, folder, barcode)
        for dic in soaked_cystal_list:
            d = get_item_as_dict(dic)
            if d['crystal_plate_barcode'] == barcode:
                if not xtbm_exists(logger, shifter_csv_file, d):
                    append_xtbm_to_shifter_csv(logger, shifter_csv_file, d)



