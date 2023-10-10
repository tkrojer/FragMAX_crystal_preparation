import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def get_soak_plate_id(dal, logger, d):
    spname = d['soak_plate_name']
    spwell = d['soak_plate_well']
    row = spwell[0]
    column = spwell[1:]
    logger.info('getting soak_plate_id for row {0!s} & column {1!s} in {2!s}'.format(row, column, spname))
    q = select(dal.soak_plate_table.c.soak_plate_id).where(and_(
               dal.soak_plate_table.c.soak_plate_name == spname,
               dal.soak_plate_table.c.soak_plate_row == row,
               dal.soak_plate_table.c.soak_plate_column == column))
    rp = dal.connection.execute(q)
    r = rp.fetchall()
    idx = r[0][0]
    logger.info('soak_plate_id = {0!s}'.format(idx))
    return idx

def get_marked_crystal_id(dal, logger, d):
    marked_crystal_code = d['marked_crystal_code']
    barcode = marked_crystal_code.split('-')[0]
    row = marked_crystal_code.split('-')[1]
    column = marked_crystal_code.split('-')[2]
    logger.info('getting marked_crystal_id for row {0!s} & column {1!s} in {2!s}'.format(row, column, barcode))
    q = select(dal.marked_crystals_table.c.marked_crystal_id).where(and_(
               dal.marked_crystals_table.c.crystal_plate_barcode == barcode,
               dal.marked_crystals_table.c.crystal_plate_row == row,
               dal.marked_crystals_table.c.crystal_plate_column == column))
    rp = dal.connection.execute(q)
    r = rp.fetchall()
    logger.info(r)
    idx = r[0][0]
    logger.info('marked_crystal_id = {0!s}'.format(idx))
    return idx

def save_soaked_crystals_to_database(logger, dal, soaked_cystal_list, base_dict, pgbar):
    logger.info('saving soaked crystal information to database')
    start, step = misc.get_step_for_progress_bar(len(soaked_cystal_list))
    for d in soaked_cystal_list:
        d.update(base_dict)
        d['soak_plate_id'] = get_soak_plate_id(dal, logger, d)
        d['marked_crystal_id'] = get_marked_crystal_id(dal, logger, d)
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
