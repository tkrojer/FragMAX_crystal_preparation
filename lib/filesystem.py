import os
from shutil import (copyfile, move)
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

def save_crystal_screen_as_excel(logger, csfolder, csname, cstemplate):
    logger.warning('removing whitespaces from crystal screen name: ' + csname)
    logger.info('trying to copy empty crystal screen EXCEL template with name ' + csname + ' to ' + csfolder)
    if os.path.isfile(os.path.join(csfolder, csname + '.xlsx')):
        logger.error('file exists in ' + os.path.join(csfolder, csname + '.xlsx'))
    else:
        logger.info('creating new template ' + os.path.join(csfolder, csname + '.xlsx'))
        df_template = pd.read_csv(cstemplate)
        df_template.to_excel(os.path.join(csfolder, csname + '.xlsx'))

def read_crystal_screen_as_df(logger, csfile):
    logger('reading {0!s} as dataframe'.format(csfile))
    df = None
    if csfile.endswith('.csv'):
        logger.info('screen file seems to be a CSV file')
        dialect = csv.Sniffer().sniff(open(csfile).readline(), [',', ';'])
        df = pd.read_csv(b.files[0], sep=dialect.delimiter)
    elif csfile.endswith('.xlsx'):
        df = pd.read_excel(csfile)
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

def save_shifter_csv_to_inspect_folder(logger, subwell_a, subwell_c, subwell_d, barcode, plate_type, folder):
    logger.info('writing CSV file for shifter inspection as ' + os.path.join(folder, '1-inspect', barcode + '.csv'))
    if os.path.isfile(os.path.join(folder, '1-inspect', barcode + '.csv')):
        self.logger.warning('file exists ' + os.path.join(folder, '1-inspect', barcode + '.csv'))
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logger.info('backing up exisiting file as ' + barcode + '.csv.' + now)
        move(os.path.join(folder, '1-inspect', barcode + '.csv'),
             os.path.join(folder, '1-inspect', 'backup', barcode + '.csv.' + now))
    csv = ''
    subwells = []
    if int(subwell_a) != 0:
        subwells.append('a')
    if int(subwell_c) != 0:
        subwells.append('c')
    if int(subwell_d) != 0:
        subwells.append('d')
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    for row in rows:
        for column in columns:
            for subwell in subwells:
                csv += '{0!s},{1!s},AM,{2!s},{3!s},{4!s},,,,,,,,,\n'.format(plate_type, barcode, row, column, subwell)
    f = open(os.path.join(folder, '1-inspect', barcode + '.csv'), 'w')
    f.write(csv)
    f.close()

def import_marked_crystals_from_shifter_csv(logger, shiftercsv):
    logger.info('loading ' + shiftercsv)
    l = []
    for line in open(shiftercsv, encoding='utf-8-sig'):
        if line.startswith(';'):
            continue
        d = {}
        d['crystal_plate_barcode'] = re.split(r'[ ,;]+', line)[1]
        d['row'] = re.split(r'[ ,;]+', line)[3]
        d['column'] = '0' * (2 - len(re.split(r'[ ,;]+', line)[4])) + re.split(r'[ ,;]+', line)[4]
        d['crystal_plate_subwell'] = re.split(r'[ ,;]+', line)[5]
        d['crystal_plate_well'] = d['row'] + d['column']
        d['marked_crystal_code'] = d['crystal_plate_barcode'] + '-' + d['crystal_plate_well'] + d['crystal_plate_subwell']
        l.append(d)
    return l

def save_marked_crystals_to_soak_folder_as_shifter_csv(logger, shiftercsv, folder):
    logger.info('saving copy of shifter csv file to 2-soak folder...')
    new_filename = shiftercsv.replace('_inspect.csv', '_crystal.csv')
    if os.path.isfile(os.path.join(folder, '2-soak', new_filename)):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logger.warning('file exists: {0!s}; moving existing file to backup folder'.format(new_filename))
        move(os.path.join(folder, '2-soak', new_filename),
             os.path.join(folder, '2-soak', 'backup', new_filename + now))
    logger.info('saving csv files as {0!a}'.format(new_filename))
    copyfile(os.path.join(folder, '1-inspect', shiftercsv),
             os.path.join(folder, '2-soak', new_filename))

def get_shifter_csv_header():
    header = [
        'PlateType',
        'PlateID',
        'LocationShifter',
        'PlateColumn',
        'PlateRow',
        'PositionSubWell',
        'Comment',
        'CrystalID',
        'TimeArrival',
        'TimeDeparture',
        'PickDuration',
        'DestinationName',
        'DestinationLocation',
        'Barcode',
        'ExternalComment'
        ]
    return header

def save_soak_plate_csv_for_shifter(logger, shifter_list, spname, folder):
    if os.path.isfile(os.path.join(folder, '2-soak', spname + '_compound.csv')):
        logger.warning('soakplate CSV file exists: ' + os.path.join(folder, '2-soak', spname + '_compound.csv'))
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logger.info(
            'moving exisiting soakplate CSV file to backup folder as: ' + spname + '_compound.csv.' + now)
        move(os.path.join(folder, '2-soak', spname + '_compound.csv'),
             os.path.join(folder, '2-soak', 'backup', spname + '_compound.csv.' + now))

    fieldnames = get_shifter_csv_header()
    with open(os.path.join(folder, '2-soak', spname + '_compound.csv'), 'w',
              encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(shifter_list)
    # need to add ";" to first line so that shifter recognises it as header
    out = ""
    with open(os.path.join(folder, '2-soak', spname + '_compound.csv')) as f:
        for n, line in enumerate(f):
            if n == 0:
                out = ";" + line
            else:
                out += line
    f = open(os.path.join(folder, '2-soak', spname + '_compound.csv'), "w")
    f.write(out)
    f.close()

def read_soaked_crystal_csv_from_shifter(logger, soak_csv):
    logger.info('reading {0!s} file...'.format(soak_csv))
    soaked_cystal_list = {}
    xtbm_list = []
    for line in open(soak_csv, encoding='utf-8-sig'):
        d = {}
        if line.startswith(';') or line.startswith('";'):
            continue
        elif line.startswith('PlateType'):
            continue
        logger.info('current line: {0!s}'.format(re.split(r'[,;]+', line)))
        # crystal_id is irrelevant, but if field is blank then nothing was transferred
        # this is not a failure but merely means that these drops were not used for soaking
        # it will however also be blank if the soak failed, but we want to capture the latter
        crystal_id = re.split(r'[,;]+', line)[7].replace(' ', '')
        if crystal_id == '' and not 'FAIL' in line:
            logger.warning('compound was not used for soaking yet; skipping...')
            continue

        try:
            d['plate_type_name'] = re.split(r'[,;]+', line)[0]
            d['soak_plate_name'] = re.split(r'[,;]+', line)[1]
            d['soak_plate_row'] = re.split(r'[,;]+', line)[3]
            d['soak_plate_column'] = '0' * (2 - len(re.split(r'[,;]+', line)[4])) + re.split(r'[,;]+', line)[4]
            d['soak_plate_subwell'] = re.split(r'[,;]+', line)[5]
            d['soak_datetime'] = re.split(r'[,;]+', line)[9]

            d['comment'] = re.split(r'[,;]+', line)[6]
            d['compound_appearance']
            d['crystal_appearance']

            if not 'FAIL' in line:
                crystal_plate_name = re.split(r'[,;]+', line)[11].replace('Right: ', '').replace('Left: ', '')
                crystal_plate_row = re.split(r'[,;]+', line)[12][0]
                crystal_plate_column = ''
                if len(re.split(r'[,;]+', line)[12]) == 3:
                    crystal_plate_column = '0' + re.split(r'[,;]+', line)[12][1]
                elif len(re.split(r'[,;]+', line)[12]) == 4:
                    crystal_plate_column = re.split(r'[,;]+', line)[12][1:3]
                crystal_plate_subwell = re.split(r'[,;]+', line)[12][-1]
                shifter_dict = {
                    'PlateType': d['plate_type_name'],
                    'PlateID': crystal_plate_name,
                    'LocationShifter': 'AM',
                    'PlateColumn': crystal_plate_column,
                    'PlateRow': crystal_plate_row,
                    'PositionSubWell': crystal_plate_subwell,
                    'ExternalComment': ''
                }
                xtbm_list.append(shifter_dict)
            else:
                logger.warning('soak failed, will not prepare xtbm csv file in 3-mount folder')
            soaked_cystal_list.append(d)

#            # save each row to csv file in 3-mount folder?
#            if crystal_plate_name not in crystal_plate_list:
#                crystal_plate_list.append(crystal_plate_name)
#                self.prepare_crystal_mount_csv_file(crystal_plate_name)
#            self.update_crystal_mount_csv_file(crystal_plate_name, plate_type, crystal_plate_row, crystal_plate_column,
#                                               crystal_plate_subwell)
#
#            # subwell is omitted for the time being since only one subwell is used for soaking
#            soakplate_condition_id = compound_plate_name + '-' + compound_plate_row + \
#                                     compound_plate_column
#
#            marked_crystal_id = crystal_plate_name + '-' + crystal_plate_row + \
#                                crystal_plate_column + crystal_plate_subwell
#
#            self.logger.info(
#                'marked crystal ID: {0!s} - soak condition ID: {1!s}'.format(marked_crystal_id, soakplate_condition_id))
#            self.update_database(soakplate_condition_id, marked_crystal_id, soak_time, comment)
        except IndexError as e:
            logger.error(e)
            continue
    return soaked_cystal_list, xtbm_list

def get_xtal_plate_list_from_shifter_dictlist(xtbm_list):
    xtal_plate_list = []
    for item in xtbm_list:
        if item['PlateID'] not in xtbm_list:
            xtal_plate_list.append(item['PlateID'])
    return xtal_plate_list

def prepare_crystal_mount_csv_for_shifter(logger, folder, xtbm_list):
    xtal_plate_list = get_xtal_plate_list_from_shifter_dictlist(xtbm_list)
    for xtal_plate in xtal_plate_list:
        if os.path.isfile(os.path.join(folder, '3-mount', xtal_plate + '_mount.csv')):
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            logger.warning('creating backup of existing {0!s}_mount.csv file in 3-mount folder'.format(xtal_plate))
            copyfile(os.path.join(folder, '3-mount', xtal_plate + '_mount.csv'),
                     os.path.join(folder, '3-mount', 'backup', xtal_plate + '_mount.csv.' + now))
        else:
            logger.info('creating {0!s}_mount.csv file in 3-mount folder'.format(xtal_plate))
            f = open(os.path.join(folder, '3-mount', xtal_plate + '_mount.csv'), 'w')
            f.write('')
            f.close()

def update_crystal_mount_csv_for_shifter(logger, folder, xtbm_list):
    xtal_plate_list = get_xtal_plate_list_from_shifter_dictlist(xtbm_list)
    for xtal_plate in xtal_plate_list:
        # check if barcode, row, column, subwell exisit
        found_well = False
        for line in open(os.path.join(folder, '3-mount', xtal_plate + '_mount.csv'), encoding='utf-8-sig'):
            if line.startswith(';'):
                continue
            if line.startswith('"'):
                continue
            if line.startswith("Column1"):
                continue
            plate_name = re.split(r'[,;]+', line)[1]
            plate_row = re.split(r'[,;]+', line)[3]
            plate_column = re.split(r'[,;]+', line)[4]
            plate_subwell = re.split(r'[,;]+', line)[5]
            if plate_name == crystal_plate_name and plate_row == row and plate_column == str(
                    int(column)) and plate_subwell == subwell:
                found_well = True
                logger.warning('crystal is already flagged for mounting in {0!a}_mount.csv: {1!s}, {2!s}, {3!s}; skipping...'.format(xtal_plate, row, str(int(column)), subwell))
        if not found_well:
            logger.info('flagging crystal for mounting in {0!a}_mount.csv: {1!s}, {2!s}, {3!s}; skipping...'.format(xtal_plate, row, column, subwell))
            f = open(os.path.join(folder, '3-mount', xtal_plate + '_mount.csv'), 'a')
            f.write('{0!s},{1!s},AM,{2!s},{3!s},{4!s},,,,,,,,,\n'.format(plate_type, xtal_plate, row, str(int(column)), subwell))
            f.close()

def read_line_from_shifter_csv(logger, line):
    if line.startswith(';'):
        s = {}
    elif line.startswith('PlateType'):
        s = {}
    elif line.startswith('";'):
        s = {}
    elif line.startswith('"'):
        s = {}
    elif line.startswith("Column1"):
        s = {}
    else:
        try:
            s = {
                'PlateType':            re.split(r'[,;]+', line)[0],
                'PlateID':              re.split(r'[,;]+', line)[1],
                'LocationShifter':      re.split(r'[,;]+', line)[2],
                'PlateRow':             re.split(r'[,;]+', line)[3],
                'PlateColumn':          re.split(r'[,;]+', line)[4],
                'PositionSubWell':      re.split(r'[,;]+', line)[5],
                'Comment':              re.split(r'[,;]+', line)[6],
                'CrystalID':            re.split(r'[,;]+', line)[7],
                'TimeArrival':          re.split(r'[,;]+', line)[8],
                'TimeDeparture':        re.split(r'[,;]+', line)[9],
                'PickDuration':         re.split(r'[,;]+', line)[10],
                'DestinationName':      re.split(r'[,;]+', line)[11],
                'DestinationLocation':  re.split(r'[,;]+', line)[12],
                'Barcode':              re.split(r'[,;]+', line)[13],
                'ExternalComment':      re.split(r'[,;]+', line)[14]
            }
        except IndexError:
            logger.warning('seems there are marked but not mounted crystals in file (check info line below):')
            logger.info(str(line.split(';')))
            s = {}
    return s

def read_mounted_crystal_csv_from_shifter(logger, crystal_csv):
    logger.info('reading shifter csv file with mounted crystals: ' + crystal_csv)
    l = []
    for line in open(shifter_csv_file, encoding='utf-8-sig'):
        d = read_line_from_shifter_csv(logger, line)
        if d:
            if 'fail' in d['Comment'].lower():
                logger.error('mounting of sample failed (check info line below); skipping...')
                logger.info(str(line.split(';')))
                continue
            else:
                l.append(d)
        else:
            logger.warning('unexpected starting string (most likely file header); ignoring line: ' + line)

#        self.logger.info(line)
#        # need to do this because excel puts a hidden \ufeff character at the beginning of the file
#        if line.startswith(';'):
#            continue
#        if line.startswith('"'):
#            continue
#        try:
#            self.logger.info(re.split(r'[,;]+', line))
#            plate_type = re.split(r'[,;]+', line)[0]
#            #                self.logger.warning(repr(plate_type))
#            if plate_type not in known_plate_types:
#                self.logger.error('cannot find plate type {0!s} in database; skipping row...'.format(plate_type))
#                continue
#            plate_name = re.split(r'[,;]+', line)[1]
#            plate_row = re.split(r'[,;]+', line)[3]
#            plate_column = '0' * (2 - len(re.split(r'[,;]+', line)[4])) + re.split(r'[,;]+', line)[4]
#            plate_well = plate_row + plate_column
#            self.logger.info('-> {0!s}'.format(plate_well))
#            plate_subwell = re.split(r'[,;]+', line)[5]
#            mount_time = re.split(r'[,;]+', line)[9]
#            comment = re.split(r'[,;]+', line)[6]
#            if 'fail' in comment.lower():
#                self.logger.error('mounting failed; skipping...')
#                continue
#            puck_name = re.split(r'[,;]+', line)[11]
#            puck_position = re.split(r'[,;]+', line)[12]
#
#            marked_crystal_id = plate_name + '-' + plate_row + \
#                                plate_column + plate_subwell
#        except IndexError:
#            self.logger.warning('seems there are marked but not mounted crystals in file:')
#            self.logger.info(str(line.split(';')))

