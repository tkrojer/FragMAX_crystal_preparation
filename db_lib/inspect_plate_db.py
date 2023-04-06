import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def get_crystal_screen_condition_id(dal, logger, row, column, plate_id):
    logger.info('gettting crystal_screen_condition_id for row & column')
    j = dal.crystal_plate_table.join(
        dal.crystal_screen_table, dal.crystal_plate_table.c.crystal_screen_id ==
                                  dal.crystal_screen_table.c.crystal_screen_id, isouter=True).join(
        dal.crystal_screen_condition_table, dal.crystal_screen_table.c.crystal_screen_id ==
                                            dal.crystal_screen_condition_table.c.crystal_screen_id, isouter=True)
    q = select(dal.crystal_screen_condition_table.c.crystal_screen_condition_id).where(and_(
        dal.crystal_screen_condition_table.c.crystal_screen_row == row,
        dal.crystal_screen_condition_table.c.crystal_screen_column == column,
        dal.crystal_plate_table.c.crystal_plate_id == plate_id))
    rp = dal.connection.execute(q)
    r = rp.fetchall()
    try:
        idx = r[0][0]
        logger.info('crystal_screen_condition_id for row & column is {0!s}'.format(idx))
    except IndexError:
        logger.error('crystal_screen_condition_id does not exist for row & column')
        idx = None
    return idx

def save_marked_crystals_to_db(dal, logger, l, pgbar, plate_id):
    logger.info('saving marked crystal entries to database')
    start, step = misc.get_step_for_progress_bar(len(l))
    for d in l:
        d['crystal_plate_id'] = plate_id
        start += step
        pgbar.value = int(start)
        row = d['crystal_plate_row']
        column = d['crystal_plate_column']
        idx = get_crystal_screen_condition_id(dal, logger, row, column, plate_id)
        if idx:
            d['crystal_screen_condition_id'] = idx
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