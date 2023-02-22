import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

import pandas as pd

def save_crystal_plate_to_database(logger, dal, d, barcode):
    logger.info('saving crystal plate {0!s} to database'.format(barcode))
    try:
        d.update({'crystal_plate_barcode': barcode})
        ins = dal.crystal_plate_table.insert().values(d)
        dal.connection.execute(ins)
    except sqlalchemy.exc.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            logger.warning('crystal plate exists in database; updating information...')
            u = dal.crystal_plate_table.update().values(d).where(dal.crystal_plate_table.c.crystal_plate_barcode == barcode)
            dal.connection.execute(u)
        else:
            logger.error(str(e))
    logger.info('finished saving crystal plate {0!s} to database'.format(barcode))

def load_crystal_plate_from_database(dal, logger, barcode):
    logger.info('loading information for crystal plate ' + barcode)
    q = select([dal.crystal_plate_table]).where(dal.crystal_plate_table.c.crystal_plate_barcode == barcode)
    rp = dal.connection.execute(q)
    plate = rp.fetchall()
    x = [dict(r) for r in plate][0]
    logger.info('finished loading information for crystal plate ' + barcode)
    return x
