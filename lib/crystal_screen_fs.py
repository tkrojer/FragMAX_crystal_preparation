import os
import csv
import pandas as pd

def save_crystal_screen_as_csv(logger, csfolder, csname, cstemplate):
    logger.warning('removing whitespaces from crystal screen name: ' + csname)
    logger.info('trying to copy empty crystal screen CSV template with name ' + csname + ' to ' + csfolder)
    if os.path.isfile(os.path.join(csfolder, csname + '.csv')):
        logger.error('file exists in ' + os.path.join(csfolder, csname + '.csv'))
    else:
        logger.info('creating new template ' + os.path.join(csfolder, csname + '.csv'))
        copyfile(cstemplate, os.path.join(csfolder, csname + '.csv'))
    logger.info('finished saving crystal screen csv')

def save_crystal_screen_as_excel(logger, csfolder, csname, cstemplate):
    logger.warning('removing whitespaces from crystal screen name: ' + csname)
    logger.info('trying to copy empty crystal screen EXCEL template with name ' + csname + ' to ' + csfolder)
    if os.path.isfile(os.path.join(csfolder, csname + '.xlsx')):
        logger.error('file exists in ' + os.path.join(csfolder, csname + '.xlsx'))
    else:
        logger.info('creating new template ' + os.path.join(csfolder, csname + '.xlsx'))
        df_template = pd.read_csv(cstemplate)
        df_template.to_excel(os.path.join(csfolder, csname + '.xlsx'), index=False)
    logger.info('finished saving crystal screen excel file')

def read_crystal_screen_as_df(logger, csfile):
    logger.info('reading {0!s} as dataframe'.format(csfile))
    df = None
    if csfile.endswith('.csv'):
        logger.info('screen file seems to be a CSV file')
        dialect = csv.Sniffer().sniff(open(csfile).readline(), [',', ';'])
        df = pd.read_csv(b.files[0], sep=dialect.delimiter)
    elif csfile.endswith('.xlsx'):
        df = pd.read_excel(csfile)
    logger.info('finished reading {0!s} as dataframe'.format(csfile))
    return df

def save_dragonfly_to_csv(logger, dragonflyFile):
    logger.info('converting dragonfly .txt file to .csv file')
    csv = 'CrystalScreen_Well,CrystalScreen_Condition\n'
    new_condition = False
    for line in open(dragonflyFile):
        if new_condition and line.replace('\n', '') == '':
            csv += well + ',' + condition[:-3] + '\n'
            new_condition = False
        if new_condition:
            condition += line.replace('\n', '').replace(',', '.') + ' - '
        if line.endswith(':\n') and not 'Components' in line:
            well = line.replace(':\n', '')
            if len(well) == 2:
                well = well[0] + '0' + well[1]
            new_condition = True
            condition = ''
    logger.info('saving dragonfly txt file as csv: ' + dragonflyFile.replace('.txt', '.csv'))
    f = open(dragonflyFile.replace('.txt', '.csv'), 'w')
    f.write(csv)
    f.close()
    logger.info('finished saving dragonfly txt file as csv file')