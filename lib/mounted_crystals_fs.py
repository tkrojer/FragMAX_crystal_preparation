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

def save_csv_file_for_exi(logger, df, csv_file):
    logger.info('saving csv file for exi as {0!s}'.format(csv_file))
    df.to_csv(csv_file, header=False, index=False)
    logger.info('finished saving csv file for exi')

def save_csv_summary_file(logger, df, csv_file):
    logger.info('saving csv summary file as {0!s}'.format(csv_file))
    df.to_csv(csv_file, header=True, index=False)
    logger.info('finished saving csv summary file')
    logger.info('saving excel summary file as {0!s}'.format(csv_file.replace('.csv', '.xlsx')))
    df.to_excel(csv_file.replace('.csv', '.xlsx'), header=True, index=False)
