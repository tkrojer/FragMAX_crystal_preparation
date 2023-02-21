import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

import pandas as pd

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
