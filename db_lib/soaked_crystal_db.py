import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def save_soaked_crystals_to_database(logger, dal, soaked_cystal_list, base_dict, pgbar):
    logger.info('saving soaked crystal information to database')
    start, step = misc.get_step_for_progress_bar(len(soaked_cystal_list))
    for d in soaked_cystal_list:
        d.update(base_dict)
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
