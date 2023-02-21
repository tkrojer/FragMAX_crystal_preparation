import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_

def get_empty_project_info():
    d = {
    'project_name': '',
    'proposal_number': '',
    'protein_name': '',
    'protein_acronym': ''
    }
    return d

def get_project_info(dal, logger):
    q = select(dal.project_table)
    rp = dal.connection.execute(q)
    result = rp.first()
    value_dict = get_empty_project_info()
    try:
        for n, key in enumerate(result.keys()):
            if result[n] == None:
                value_dict[key] = ''
            else:
                value_dict[key] = result[n]
        logger.warning('project information: {0!s}'.format(value_dict))
    except AttributeError:
        logger.warning('missing project information')
    return value_dict

def save_project_info(dal, logger, d):
    try:
        logger.info('creating new entry for project information')
        ins = dal.project_table.insert().values(d)
        dal.connection.execute(ins)
    except sqlalchemy.exc.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            logger.warning('updating existing project information entry')
            u = dal.project_table.update().values(d).where(dal.project_table.c.project_id == 1)
            dal.connection.execute(u)
        else:
            logger.error(str(e))
