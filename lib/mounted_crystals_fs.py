import os
import pandas as pd

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def get_shifter_csv_file_as_dict_list(logger, shifter_csv_file):
    xtal_list = []
    soak_list = []
    for line in open(shifter_csv_file, encoding='utf-8-sig'):
        mount_dict, soak_dict = misc.read_line_from_shifter_csv_as_mounted_crystal_dict(logger, line)
        if mount_dict:
            xtal_list.append(mount_dict)
        if soak_dict:
            soak_list.append(soak_dict)
    return xtal_list, soak_list

def get_manual_excel_file_as_dict_list(logger, manual_excel_file):
    soak_list = []
    logger.info('reading {0!s} as list of dicts...'.format(manual_excel_file))
    df = pd.read_excel(manual_excel_file)
#    df['marked_crystal_code'] = df[['crystal_plate_barcode',
#                                    'crystal_plate_row',
#                                    'crystal_plate_column',
#                                    'subwell']].agg('-'.join, axis=1)

    df['marked_crystal_code'] = df['crystal_plate_barcode'].astype(str) + "-" + \
                                df['crystal_plate_row'] + "-" + \
                                df['crystal_plate_column'].astype(str) + "-" + \
                                df['subwell'].astype(str)

    df = df.drop('crystal_plate_barcode', axis=1)
    df = df.drop('crystal_plate_row', axis=1)
    df = df.drop('crystal_plate_column', axis=1)
    df = df.drop('subwell', axis=1)
    df['mount_datetime'] = pd.to_datetime(df['mount_datetime'])
    #df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y')
    xtal_list = df.to_dict('records')
    return xtal_list, soak_list

def save_csv_file_for_exi(logger, df, csv_file):
    logger.info('saving csv file for exi as {0!s}'.format(csv_file))
    df.to_csv(csv_file, header=False, index=False)
    logger.info('finished saving csv file for exi')

def save_csv_summary_file(logger, dfsumm, dfproc, csv_file, process_csv):
    logger.info('saving csv summary file as {0!s}'.format(csv_file))
    dfsumm.to_csv(csv_file, header=True, index=False)
    logger.info('finished saving csv summary file')
    logger.info('saving excel summary file as {0!s}'.format(csv_file.replace('.csv', '.xlsx')))
    dfsumm.to_excel(csv_file.replace('.csv', '.xlsx'), header=True, index=False)
#    dfproc = dfproc.drop_duplicates(subset=['mounted_crystal_code'], keep='last')
    logger.info('saving csv file for processing (only unique mounted_crystal_codes)')
    dfproc.to_csv(process_csv, header=True, index=False)

def save_csv_file_for_fragmaxapp(logger, df, csv_file):
    logger.info('saving csv file for fragmaxapp as {0!s}'.format(csv_file))
    df.to_csv(csv_file, header=False, index=False)
    logger.info('finished saving csv file for fragmaxapp')

def save_manual_mount_template(logger, folder, now, excel_file):
    logger.info('saving excel file template for manually mounted crystals as {0!s}'.format(excel_file))

    data = [['', '', '', '', '', '', '', '', now]]

    df = pd.DataFrame(data, columns=['manual_mounted_crystal_code',
                                     'puck_name',
                                     'puck_position',
                                     'crystal_plate_barcode',
                                     'crystal_plate_row',
                                     'crystal_plate_column',
                                     'subwell',
                                     'data_collection_comment',
                                     'mount_datetime'])
    df.to_excel(excel_file, header=True, index=False)
