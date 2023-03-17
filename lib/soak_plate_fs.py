import os
import pandas as pd

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def save_soak_plate_csv_file(logger, folder, soak_plate_name, df):
    logger.info('writing soak plate CSV file as ' + os.path.join(folder, '2-soak', soak_plate_name + '_soak.csv'))
    misc.backup_file(logger, os.path.join(folder, '2-soak'), soak_plate_name + '_soak.csv')
    df['status'] = 'pending'
    df.to_csv(os.path.join(os.path.join(folder, '2-soak', soak_plate_name + '_soak.csv')), index=False)
    logger.info('finished writing soak plate CSV file')