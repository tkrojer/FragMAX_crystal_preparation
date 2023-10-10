import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_
import pandas as pd

import os, sys
sys.path.append(os.path.join(os.getcwd(), 'db_lib'))
import query

def save_protein_batch_to_db(dal, logger, l):
    logger.info('creating new protein batch')
    for d in l:
        try:
            ins = dal.protein_batch_table.insert().values(d)
            dal.connection.execute(ins)
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('updating existing protein batch entry')
                u = dal.protein_batch_table.update().values(d)
                u = u.where(dal.protein_batch_table.c.protein_batch_name == d['protein_batch_name'])
                dal.connection.execute(u)
            else:
                logger.error(str(e))
    logger.info('finished creating new protein batch')

def get_protein_batches_from_db(dal, logger):
    logger.info('reading protein batch information from database')
    q = select(dal.protein_batch_table).order_by(dal.protein_batch_table.c.protein_batch_id.asc())
    rp = dal.connection.execute(q)
    result = rp.fetchall()
    result_list = query.get_result_list_of_dicts(result)
    logger.info('finished reading protein batch information from database')
    return result_list

def get_organism_list_from_db(dal, logger):
    logger.info('reading list of organisms from database')
    q = select(dal.gene_src_table.c.pdbx_gene_src_scientific_name)
    rp = dal.connection.execute(q)
    result_list = [x[0] for x in rp.fetchall()]
    logger.info('finished reading organism list information from database')
    return result_list

def get_comp_id_info_as_df(dal, logger):
    logger.info('reading comp_id information as dataframe from database')
    q = select([dal.wwpdb_chem_comp_table.c.chem_comp_code,
                dal.wwpdb_chem_comp_table.c.name,
                dal.wwpdb_chem_comp_table.c.popular_name])
    df = pd.read_sql_query(q, dal.engine)
    df = df.replace(r'\\n', ' ', regex=True)    # since there may be hidden characters
    logger.info('finished reading comp_id information as dataframe from database')
    return df

