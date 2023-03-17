import sqlalchemy
from sqlalchemy.sql import select, cast
from sqlalchemy import and_, Integer

import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def save_soak_plate_to_database(logger, dal, dbase, pgbar):
    logger.info('saving soak plate {0!s} to database'.format(dbase['compound_plate_name']))
    q = select([dal.compound_batch_table.c.compound_plate_row,
                dal.compound_batch_table.c.compound_plate_column,
                dal.compound_batch_table.c.compound_batch_code,
                dal.compound_batch_table.c.compound_plate_name]).where(
                dal.compound_batch_table.c.compound_plate_name == dbase['compound_plate_name'])
    rp = dal.connection.execute(q)
    results = rp.fetchall()
    start, step = misc.get_step_for_progress_bar(len(results))
    for r in results:
        start += step
        pgbar.value = int(start)
        d = dbase
        d['soak_plate_row'] = r[0]
        d['soak_plate_column'] = r[1]
        d['soak_plate_well'] = r[0] + str(int(r[1]))
        d['compound_batch_code'] = r[2]
        d['compound_plate_name'] = r[3]
        try:
            ins = dal.soak_plate_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('soak plate well exists in database; updating information...')
                u = dal.soak_plate_table.update().values(d).where(and_(
                    dal.soak_plate_table.c.soak_plate_name == d['soak_plate_name'],
                    dal.soak_plate_table.c.soak_plate_well == d['soak_plate_well']))
                dal.connection.execute(u)
            else:
                logger.error(str(e))
    pgbar.value = 0
    logger.info('finished saving soak plate {0!s} to database'.format(dbase['compound_plate_name']))

def get_soak_plate_from_database_as_df(logger, dal, soak_plate_name):
    logger.info('reading soak plate {0!s} from database'.format(soak_plate_name))
    q = select([dal.soak_plate_table.c.soak_plate_name,
                dal.soak_plate_table.c.soak_plate_type,
                dal.soak_plate_table.c.soak_plate_well,
                dal.soak_plate_table.c.soak_plate_row,
                dal.soak_plate_table.c.soak_plate_column]).where(
                dal.soak_plate_table.c.soak_plate_name == soak_plate_name).order_by(
                cast(dal.soak_plate_table.c.soak_plate_column, Integer).asc(),
                dal.soak_plate_table.c.soak_plate_row.asc()
    )
    df = pd.read_sql_query(q, dal.engine)
    # soak_plate_column and soak_plate_column are only needed for proper sorting for CSV file
    # otherwise it looks like A1, A10, A11, A12, A2...
    del df['soak_plate_row']
    del df['soak_plate_column']
    df['marked_crystal_code'] = ''
    logger.info('finished reading soak plate {0!s} from database'.format(soak_plate_name))
    return df
