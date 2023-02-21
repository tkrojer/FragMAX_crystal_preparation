import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

import pandas as pd

def save_soak_plate_to_database(logger, dal, dbase):
    logger.info('saving soak plate {0!s} to database'.format(dbase['compound_plate_name']))
    q = select([dal.compound_batch_table.c.compound_plate_well,
                dal.compound_batch_table.c.compound_batch_id]).where(
                dal.compound_batch_table.c.compound_plate_name == dbase['compound_plate_name'])
    rp = dal.connection.execute(q)
    results = rp.fetchall()
    for r in results:
        d['soak_plate_well'] = r[0]
        d['soak_plate_column'] = d['soak_plate_well'][0]
        d['soak_plate_row'] = d['soak_plate_well'][1:3]
        d = dbase
        d['compound_batch_id'] = r[1]
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

def get_soak_plate_from_database_as_df(logger, dal, soak_plate_name):
    logger.info('reading soak plate {0!s} from database'.format(soak_plate_name))
    q = select([dal.soak_plate_table.c.soak_plate_name,
                dal.soak_plate_table.c.soak_plate_type,
                dal.soak_plate_table.c.soak_plate_well]).where(
                dal.soak_plate_table.c.soak_plate_name == soak_plate_name)
    df = pd.read_sql_query(q, dal.engine)
    df['marked_crystal_code'] = ''
    return df
