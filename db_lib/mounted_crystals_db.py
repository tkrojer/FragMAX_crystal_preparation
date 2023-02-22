import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

import pandas as pd


def get_next_mounted_crystal_number(logger, dal):
    q = select(dal.mounted_crystals_table.c.mounted_crystal_code).order_by(
               dal.mounted_crystals_table.c.mounted_crystal_code.desc()).limit(1)
    rp = dal.connection.execute(q)
    result = rp.fetchall()
    if result:
        mcc = result[0][0]
        next = int(mcc.split('-')[len(mcc.split('-'))-1].replace('x','')) + 1
        logger.info('mounted_crystal_code of last mounted crystal: {0!s}'.format(mcc))
    else:
        next = 1
        logger.warning('seems like no crystals were mounted yet')
    logger.info('next crystal will be number {0!s}'.format(next))
    return next

def get_mounted_crystal_code(proteinacronym, next):
    mounted_crystal_code = proteinacronym + '-x' + ((4-len(str(next))) * '0') + str(next)
    return mounted_crystal_code

def save_mounted_crystals_to_database(logger, dal, xtal_list, proteinacronym, pgbar):
    logger.info('saving mounted crystals to database')
    next = get_next_mounted_crystal_number(logger, dal)
    start, step = misc.get_step_for_progress_bar(len(xtal_list))
    for d in xtal_list:
        start += step
        pgbar.value = int(start)
        try:
            d['mounted_crystal_code'] = get_mounted_crystal_code(proteinacronym, next)
            logger.info('current crystal: {0!s}'.format(d['mounted_crystal_code']))
            ins = dal.mounted_crystals_table.insert().values(d)
            dal.connection.execute(ins)
            next += 1
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('mounted crystal exists; skipping...')
            else:
                logger.error(str(e))
    pgbar.value = 0
    logger.info('finished inserting samples into mounted_crystals_table')

def update_soeked_crystal_table(logger, dal, soak_list, pgbar):
    logger.info('updating soaked crystals table in database')
    start, step = misc.get_step_for_progress_bar(len(soak_list))
    for d in soak_list:
        start += step
        pgbar.value = int(start)
        try:
            u = dal.soaked_crystals_table.update().values(d).where(
                dal.soaked_crystals_table.c.marked_crystal_code == d['marked_crystal_code'])
            dal.connection.execute(u)
        except Exception as e:
            logger.error(str(e))
    pgbar.value = 0
    logger.info('finished updating soaked_crystals_table')

def get_mounted_crystals_from_db_for_table_as_df(logger, dal):
    logger.info('reading mounted crystals from database')
    if dal.conn_string is not None:
        q = select([dal.mounted_crystals_table.c.mounted_crystal_code,
                    dal.mounted_crystals_table.c.puck_name,
                    dal.mounted_crystals_table.c.puck_position,
                    dal.mounted_crystals_table.c.shipment]).order_by(
                    dal.mounted_crystals_table.c.mounted_crystal_code.asc())
        df = pd.read_sql_query(q, dal.engine)
    else:
        logger.info('database not initialised; using blank values...')
        header = ['mounted_crystal_code', 'puck_name', 'puck_position', 'shipment']
        data = []
        for i in range(10):
            row = []
            for j in range(len(header)):
                row.append("............")
            data.append(row)
        df = pd.DataFrame(data, columns=[header])
    logger.info('finished reading mounted crystals from database')
    return df