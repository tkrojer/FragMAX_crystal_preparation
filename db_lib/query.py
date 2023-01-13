import sqlalchemy
from sqlalchemy.sql import select

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

def get_protein_acronym(dal, logger):
    q = select(dal.project_table.c.protein_acronym)
    rp = dal.connection.execute(q)
    result = rp.first()
    proteinacronym = result[0]
    return proteinacronym

def save_protein_batch_to_db(dal, logger, l):
    for d in l:
        try:
            logger.info('creating new protein batch')
            ins = dal.protein_batch_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('updating existing protein batch entry')
                u = dal.protein_batch_table.update().values(d)
                u = u.where(dal.protein_batch_table.c.protein_batch_id == d['protein_batch_id'])
                dal.connection.execute(u)
            else:
                logger.error(str(e))

def get_result_list_of_dicts(result):
    result_list = []
    for entry in result:
        value_dict = {}
        for n, key in enumerate(entry.keys()):
            if entry[n] == None:
                value_dict[key] = ''
            else:
                value_dict[key] = entry[n]
        result_list.append(value_dict)
    return result_list

def get_protein_batches_from_db(dal, logger):
    logger.info('reading protein batch information from database')
    q = select(dal.protein_batch_table).order_by(dal.protein_batch_table.c.protein_batch_id.asc())
    rp = dal.connection.execute(q)
    result = rp.fetchall()
    result_list = get_result_list_of_dicts(result)
    return result_list

