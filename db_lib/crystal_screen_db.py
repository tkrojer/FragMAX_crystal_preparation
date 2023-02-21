import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

import pandas as pd

def get_crystal_screen_conditions_as_df(dal, logger, crystal_screen_name):
    logger.info('loading information for screen {0!s} from database'.format(crystal_screen_name))
    q = select([dal.crystal_screen_table.c.crystal_screen_well,
                dal.crystal_screen_table.c.crystal_screen_condition]).where(
                dal.crystal_screen_table.c.crystal_screen_name == crystal_screen_name)
    df = pd.read_sql_query(q, dal.engine)
    return df

def save_crystal_screen_to_db(dal, logger, df, csname, pgbar):
    logger.info('saving ' + csname + ' crystal screen to database')
    start, step = get_step_for_progress_bar(len(df.index))
    for index, row in df.iterrows():
        start += step
        pgbar.value = int(start)
        d = {
        'crystal_screen_condition': df.at[index, 'crystal_screen_condition'],
        'crystal_screen_well': df.at[index, 'crystal_screen_well']
        }
        try:
            d.update({'crystal_screen_name': csname})
            ins = dal.crystal_screen_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('crystal screen exists in database; updating information...')
                del d['crystal_screen_name']
                well = d['crystal_screen_well']
                del d['crystal_screen_well']
                u = dal.crystal_screen_table.update().values(d).where(and_(
                    dal.crystal_screen_table.c.crystal_screen_name == csname,
                    dal.crystal_screen_table.c.crystal_screen_well == well))
                dal.connection.execute(u)
            else:
                logger.error(str(e))
    pgbar.value = 0

