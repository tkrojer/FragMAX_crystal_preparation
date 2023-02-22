import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def save_marked_crystals_to_db(dal, logger, l, pgbar):
    logger.info('saving marked crystal entries to database')
    start, step = misc.get_step_for_progress_bar(len(l))
    for d in l:
        start += step
        pgbar.value = int(start)
        try:
            logger.info('creating new marked crystal entry')
            ins = dal.marked_crystals_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('marked crystal entry exists; skipping...')
#                logger.warning('updating existing protein batch entry')
#                u = dal.marked_crystals_table.update().values(d)
#                u = u.where(dal.marked_crystals_table.c.crystal_plate_barcode == d['crystal_plate_barcode'])
#                dal.connection.execute(u)
            else:
                logger.error(str(e))
    pgbar.value = 0
    logger.info('finished saving marked crystal entries to database')