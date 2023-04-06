import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def get_crystal_screen_conditions_as_df(dal, logger, crystal_screen_name):
    logger.info('loading information for screen {0!s} from database'.format(crystal_screen_name))
    q = select([dal.crystal_screen_table.c.crystal_screen_well,
                dal.crystal_screen_table.c.crystal_screen_condition]).where(
                dal.crystal_screen_table.c.crystal_screen_name == crystal_screen_name)
    df = pd.read_sql_query(q, dal.engine)
    logger.info('finished loading information for screen {0!s} from database'.format(crystal_screen_name))
    return df

def save_crystal_screen_to_db(dal, logger, df, csname, pgbar):
    logger.info('saving ' + csname + ' crystal screen information to database')
    csid = update_crystal_screen_table(dal, logger, csname)
    update_crystal_screen_condition_table(dal, logger, df, csname, csid, pgbar)

def get_crystal_screen_id(dal, logger, csname):
    logger.info('crystal_screen_id is None, but will check if crystal_screen_name_exists')
    q = select(dal.crystal_screen_table.c.crystal_screen_id).where(
               dal.crystal_screen_table.c.crystal_screen_name == csname)
    rp = dal.connection.execute(q)
    r = rp.fetchall()
    try:
        idx = r[0][0]
    except IndexError:
        logger.info('crystal_screen_name {0!s} does not exist'.format(csname))
        idx = None
    return idx

def update_crystal_screen_table(dal, logger, csname):
    logger.warning('adding screen {0!s} to crystal_screen_table'.format(csname))
    csid = get_crystal_screen_id(dal, logger, csname)
    if csid == None:
        d = {}
        d['crystal_screen_name'] = csname
        ins = dal.crystal_screen_table.insert().values(d)
        result = dal.connection.execute(ins)
        csid = result.lastrowid
        logger.info('crystal_screen_id is {0!s}'.format(csid))
    else:
        logger.warning('screen {0!s} exists in crystal_screen_table'.format(csname))
    logger.warning('finished adding screen {0!s} to crystal_screen_table'.format(csname))
    return csid

def update_crystal_screen_condition_table(dal, logger, df, csname, csid, pgbar):
    logger.warning('adding crystallization conditions to crystal_screen_condition_table')
    start, step = misc.get_step_for_progress_bar(len(df.index))
    for index, row in df.iterrows():
        start += step
        pgbar.value = int(start)
        d = {}
        d['crystal_screen_id'] = csid
        d['crystal_screen_condition'] = df.at[index, 'crystal_screen_condition']
        d['crystal_screen_well'] = df.at[index, 'crystal_screen_well']
        d['crystal_screen_row'] = df.at[index, 'crystal_screen_well'][0]
        d['crystal_screen_column'] = str(int(df.at[index, 'crystal_screen_well'][1:3]))
#        d = {
#        'crystal_screen_id': csid,
#        'crystal_screen_condition': df.at[index, 'crystal_screen_condition'],
#        'crystal_screen_well': df.at[index, 'crystal_screen_well'],
#        'crystal_screen_row' = df.at[index, 'crystal_screen_well'][0],
#        'crystal_screen_column' = str(int(df.at[index, 'crystal_screen_well'][1:3]))
#        }
        try:
#            d.update({'crystal_screen_name': csname})
            ins = dal.crystal_screen_condition_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('crystal screen exists in database; updating information...')
                idx = d['crystal_screen_id']
                row = d['crystal_screen_row']
                col = d['crystal_screen_column']
                condition = d['crystal_screen_condition']
                d = {}
                d['crystal_screen_condition'] = condition
                u = dal.crystal_screen_condition_table.update().values(d).where(and_(
                    dal.crystal_screen_condition_table.c.crystal_screen_id == idx,
                    dal.crystal_screen_condition_table.c.crystal_screen_row == row,
                    dal.crystal_screen_condition_table.c.crystal_screen_column == col))
                dal.connection.execute(u)
            else:
                logger.error(str(e))
    pgbar.value = 0
    logger.warning('finished adding crystallization conditions to crystal_screen_condition_table')
