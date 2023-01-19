import sqlalchemy
from sqlalchemy.sql import select
import pandas as pd

def get_empty_project_info():
    d = {
    'project_name': '',
    'proposal_number': '',
    'protein_name': '',
    'protein_acronym': ''
    }
    return d

def get_step_for_progress_bar(steps):
    start = 0.0
    step = float(100/int(steps))
    return start, step

def get_project_info(dal, logger):
    q = select(dal.project_table)
    rp = dal.connection.execute(q)
    result = rp.first()
    value_dict = get_empty_project_info()
    try:
        for n, key in enumerate(result.keys()):
            if result[n] == None:
                value_dict[key] = ''
            else:
                value_dict[key] = result[n]
        logger.warning('project information: {0!s}'.format(value_dict))
    except AttributeError:
        logger.warning('missing project information')
    return value_dict

def save_project_info(dal, logger, d):
    try:
        logger.info('creating new entry for project information')
        ins = dal.project_table.insert().values(d)
        dal.connection.execute(ins)
    except sqlalchemy.exc.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            logger.warning('updating existing project information entry')
            u = dal.project_table.update().values(d).where(dal.project_table.c.project_id == 1)
            dal.connection.execute(u)
        else:
            logger.error(str(e))

def get_protein_acronym(dal, logger):
    q = select(dal.project_table.c.protein_acronym)
    rp = dal.connection.execute(q)
    result = rp.first()
    proteinacronym = result[0]
    return proteinacronym

def save_protein_batch_to_db(dal, logger, l):
    for d in l:
        try:
            logger.info('creating new protein batch')
            ins = dal.protein_batch_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('updating existing protein batch entry')
                u = dal.protein_batch_table.update().values(d)
                u = u.where(dal.protein_batch_table.c.protein_batch_id == d['protein_batch_id'])
                dal.connection.execute(u)
            else:
                logger.error(str(e))

def get_result_list_of_dicts(result):
    result_list = []
    for entry in result:
        value_dict = {}
        for n, key in enumerate(entry.keys()):
            if entry[n] == None:
                value_dict[key] = ''
            else:
                value_dict[key] = entry[n]
        result_list.append(value_dict)
    return result_list

def get_protein_batches_from_db(dal, logger):
    logger.info('reading protein batch information from database')
    q = select(dal.protein_batch_table).order_by(dal.protein_batch_table.c.protein_batch_id.asc())
    rp = dal.connection.execute(q)
    result = rp.fetchall()
    result_list = get_result_list_of_dicts(result)
    return result_list

def get_crystal_screen_conditions_as_df(dal, logger, crystal_screen_name):
    logger.info('loading information for screen {0!s} from database'.format(crystal_screen_name))
    q = select([dal.crystal_screen_table.c.crystal_screen_well,
                dal.crystal_screen_table.c.crystal_screen_condition]).where(
                dal.crystal_screen_table.c.crystal_screen_name == crystal_screen_name)
    df = pd.read_sql_query(q, dal.engine)
    return df

def save_crystal_screen_to_db(dal, logger, df, csname, pgbar):
    logger.info('saving ' + csname + ' crystal screen to database')
    start, step = get_step_for_progress_bar(len(df.index))
    for index, row in df.iterrows():
        start += step
        pgbar.value = int(start)
        d = {
        'crystal_screen_condition': df.at[index, 'CrystalScreen_Condition'],
        'crystal_screen_well': df.at[index, 'CrystalScreen_Well']
        }
        try:
            ins = dal.crystal_screen_table.insert().values(d.update({'crystal_screen_name': csname}))
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('crystal screen exists in database; updating information...')
                u = dal.crystal_screen_table.update().where(dal.crystal_screen_table.c.crystal_screen_name == csname)
                u.values(d)
                dal.connection.execute(u)
            else:
                logger.error(str(e))
    pgbar.value = 0

def get_existing_crystal_plate_barcodes(dal, logger):
    logger.info('reading existing crystal plate barcodes from database')
    q = select([dal.crystal_plate_table.c.crystal_plate_barcode.distinct()])
    rp = dal.connection.execute(q)
    existing_crystalscreens = [x[0] for x in rp.fetchall()]
    return existing_crystalscreens

def get_value_from_foreign_key(dal, column, foreignkey, key):
    q = select([column]).where(foreignkey == key)
    rp = dal.connection.execute(q)
    result = rp.fetchall()
    return result[0][0]

def get_protein_batch_for_dropdown(dal, logger):
    logger.info('reading protein batch information from database')
    q = select([dal.protein_batch_table.c.protein_batch_id,
                dal.protein_batch_table.c.protein_batch_date_received]).order_by(
        dal.protein_batch_table.c.protein_batch_id.asc())
    rp = dal.connection.execute(q)
    result = rp.fetchall()
    result_list = []
    for entry in result:
        protein_id = entry[0]
        protein_batch_date_received = entry[1]
        date_received = protein_batch_date_received.strftime('%Y-%m-%d')
        protein_acronym = get_value_from_foreign_key(dal, dal.project_table.c.protein_acronym,
                                                     dal.project_table.c.project_id,
                                                     protein_id)
        result_list.append('{0!s}: {1!s}-{2!s} ({3:s})'.format(protein_id, protein_acronym, protein_id, date_received))
    return result_list

def combine_pkey_and_name_for_dropdown(logger, dal, q):
    rp = dal.connection.execute(q)
    result = rp.fetchall()
    result_list = []
    for entry in result:
        result_list.append('{0!s}: {1!s}'.format(entry[0], entry[1]))
    return result_list

def get_existing_crystal_screens_for_dropdown(dal, logger):
    logger.info('reading existing crystal screens from database')
    q = select([dal.crystal_screen_table.c.crystal_screen_id,
                dal.crystal_screen_table.c.crystal_screen_name]).order_by(
        dal.crystal_screen_table.c.crystal_screen_id.asc())
#    rp = dal.connection.execute(q)
#    result = rp.fetchall()
#    result_list = []
#    for entry in result:
#        logger.info('>>>> {0!s}'.format(entry))
#        result_list.append('{0!s}: {1!s}'.format(entry[0], entry[1]))
    result_list = combine_pkey_and_name_for_dropdown(logger, dal, q)
    return result_list

def get_plate_type_for_dropdown(dal, logger):
    logger.info('reading plate type information from database')
    q = select([dal.plate_type_table.c.plate_type_id,
                dal.plate_type_table.c.plate_type_name]).order_by(
        dal.plate_type_table.c.plate_type_id.asc())
#    rp = dal.connection.execute(q)
#    result = rp.fetchall()
#    result_list = []
#    for entry in result:
#        logger.info('>>>> {0!s}'.format(entry))
#        result_list.append('{0!s}: {1!s}'.format(entry[0], entry[1]))
    result_list = combine_pkey_and_name_for_dropdown(logger, dal, q)
    return result_list

def get_crystallization_method_for_dropdown(dal, logger):
    logger.info('reading crystallization method information from database')
    q = select([dal.crystallization_method_table.c.method_id,
                dal.crystallization_method_table.c.method_name]).order_by(
        dal.crystallization_method_table.c.method_id.asc())
#    rp = dal.connection.execute(q)
#    result = rp.fetchall()
#    result_list = []
#    for entry in result:
#        logger.info('>>>> {0!s}'.format(entry))
#        result_list.append('{0!s}: {1!s}'.format(entry[0], entry[1]))
    result_list = combine_pkey_and_name_for_dropdown(logger, dal, q)
    return result_list

def get_soak_plates_for_dropdown(dal, logger):
    logger.info('reading soak plate entries from database')
    q = select(dal.soak_plate_table.c.soak_plate_name.distinct())
    # not sure, need to test
    rp = dal.connection.execute(q)
    return rp

def get_compound_plates_for_dropdown(dal, logger):
    logger.info('reading soak plate entries from database')
    q = select(dal.compound_batch_table.c.compound_plate_name.distinct())
    # not sure, need to test
    rp = dal.connection.execute(q)
    return rp

def save_crystal_plate_to_database(logger, dal, d, barcode):
    logger.info('saving crystal plate {0!s} to database'.format(barcode))
    try:
        ins = dal.crystal_plate_table.insert().values(d.update({'crystal_plate_barcode': barcode}))
        dal.connection.execute(ins)
    except sqlalchemy.exc.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            logger.warning('crystal plate exists in database; updating information...')
            u = dal.crystal_plate_table.update().where(dal.crystal_plate_table.c.crystal_plate_barcode == barcode)
            u.values(d)
            dal.connection.execute(u)
        else:
            logger.error(str(e))

def load_crystal_plate_from_database(dal, logger, barcode):
    logger.info('loading information for crystal plate ' + barcode)
    q = select([dal.crystal_plate_table]).where(dal.crystal_plate_table.c.crystal_plate_barcode == barcode)
    rp = dal.connection.execute(q)
    plate = rp.fetchall()
    x = [dict(r) for r in plate][0]
    return x

def save_marked_crystals_to_db(dal, logger, l):
    for d in l:
        try:
            logger.info('creating new marked crystal entry')
            ins = dal.marked_crystals_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            logger.warning('marked crystal entry exists; skipping...')
#            if "UNIQUE constraint failed" in str(e):
#                logger.warning('updating existing protein batch entry')
#                u = dal.marked_crystals_table.update().values(d)
#                u = u.where(dal.marked_crystals_table.c.crystal_plate_barcode == d['crystal_plate_barcode'])
#                dal.connection.execute(u)
#            else:
#                logger.error(str(e))

def save_soak_plate_to_database(logger, dal, dbase):
    logger.info('saving soak plate {0!s} to database'.format(dbase['compound_plate_name']))
    q = select([dal.compound_batch_table.c.compound_plate_well,
                dal.compound_batch_table.c.compound_batch_id]).where(
                dal.compound_batch_table.c.compound_plate_name == dbase['compound_plate_name'])
    rp = dal.connection.execute(q)
    results = rp.fetchall()
    shifter_list = []
    for r in results:
        d['soak_plate_well'] = r[0]
        d['soak_plate_column'] = d['soak_plate_well'][0]
        d['soak_plate_row'] = d['soak_plate_well'][1:3]
        d = dbase
        d['compound_batch_id'] = r[1]
        soak_plate_condition = dbase['soak_plate_name'] + '-' + d['soak_plate_well']
        shifter_dict = {
                'PlateType': 'SwissCI-MRC-3d',
                'PlateID': d['soak_plate_name'],
                'LocationShifter': 'AM',
                'PlateColumn': d['soak_plate_column'],
                'PlateRow': d['soak_plate_row'],
                'PositionSubWell': 'a',
                'ExternalComment': d['compound_batch_id']
        }
        shifter_list.append(shifter_dict)
        try:
            ins = dal.soak_plate_table.insert().values(d.update({'soak_plate_condition': soak_plate_condition}))
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('soak plate well exists in database; updating information...')
                u = dal.soak_plate_table.update().where(
                    dal.soak_plate_table.c.soak_plate_condition == soak_plate_condition)
                u.values(d)
                dal.connection.execute(u)
            else:
                logger.error(str(e))
    return shifter_list

def save_soaked_crystals_to_database(logger, dal, soaked_cystal_list, pgbar):
    logger.info('saving soaked crystal information to database')
    start, step = get_step_for_progress_bar(len(soaked_cystal_list))
    for d in soaked_cystal_list:
        start += step
        pgbar.value = int(start)
        try:
            ins = dal.soaked_crystals_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('entry exists (time soaked {0!s}); skipping'.format(d['soak_datetime']))
            else:
                logger.error(str(e))
        start += step
    pgbar.value = 0