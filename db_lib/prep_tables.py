import sqlalchemy
import pandas as pd
import csv

def get_dict_from_excel_sheet(standard_table_file, index):
    df = pd.read_excel(standard_table_file, index)
    value_dict = df.to_dict(orient='records')
    return value_dict

def insert(dal, standard_table_file, logger):
    standard_table_dict = {
        0: dal.unit_table,
        1: dal.plate_type_table,
        2: dal.crystallization_method_table,
        3: dal.soak_method_table,
        4: dal.space_group_table,
        5: dal.compound_table,
        6: dal.compound_batch_table
    }

    for index in standard_table_dict:
        tableObject = standard_table_dict[index]
        logger.info('preparing {0!s}... '.format(tableObject.name))
        value_dict = get_dict_from_excel_sheet(standard_table_file, index)
        for row in value_dict:
            try:
                ins = tableObject.insert().values(row)
                dal.connection.execute(ins)
            except sqlalchemy.exc.IntegrityError as e:
                if not "UNIQUE constraint failed" in str(e):
                    logger.error(str(e))
#                if "UNIQUE constraint failed" in str(e):
#                    logger.warning('entry {0!s} exists; skipping...'.format(row))
#                else:
#                    logger.error(str(e))
    logger.info('finshed preparing {0!s}... '.format(tableObject.name))
