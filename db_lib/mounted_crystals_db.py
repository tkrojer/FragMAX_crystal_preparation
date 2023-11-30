import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import and_, or_

import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def get_next_mounted_crystal_number(logger, dal):
    q = select(dal.mounted_crystals_table.c.mounted_crystal_code).order_by(
               dal.mounted_crystals_table.c.mounted_crystal_code.desc()).limit(1)
    rp = dal.connection.execute(q)
    result = rp.fetchall()
    if result:
        mcc = result[0][0]
        next = int(mcc.split('-')[len(mcc.split('-'))-1].replace('x','')) + 1
        logger.info('mounted_crystal_code of last mounted crystal: {0!s}'.format(mcc))
    else:
        next = 1
        logger.warning('seems like no crystals were mounted yet')
    logger.info('next crystal will be number {0!s}'.format(next))
    return next

def get_mounted_crystal_code(proteinacronym, next):
    mounted_crystal_code = proteinacronym + '-x' + ((4-len(str(next))) * '0') + str(next)
    return mounted_crystal_code

def get_marked_crystal_id(dal, logger, d):
    marked_crystal_code = d['marked_crystal_code']
    barcode = marked_crystal_code.split('-')[0]
    row = marked_crystal_code.split('-')[1]
    column = marked_crystal_code.split('-')[2]
    logger.info('getting marked_crystal_id for marked_crystal_code {0!s}'.format(marked_crystal_code))
    q = select(dal.marked_crystals_table.c.marked_crystal_id).where(and_(
               dal.marked_crystals_table.c.crystal_plate_barcode == barcode,
               dal.marked_crystals_table.c.crystal_plate_row == row,
               dal.marked_crystals_table.c.crystal_plate_column == column))
    rp = dal.connection.execute(q)
    r = rp.fetchall()
    idx = r[0][0]
    logger.info('marked_crystal_id = {0!s}'.format(idx))
    return idx

def save_mounted_crystals_to_database(logger, dal, xtal_list, proteinacronym, pgbar):
    logger.info('saving mounted crystals to database')
    next = get_next_mounted_crystal_number(logger, dal)
    start, step = misc.get_step_for_progress_bar(len(xtal_list))
    for d in xtal_list:
        start += step
        pgbar.value = int(start)
        try:
            d['marked_crystal_id'] = get_marked_crystal_id(dal, logger, d)
            d['mounted_crystal_code'] = get_mounted_crystal_code(proteinacronym, next)
            logger.info('current crystal: {0!s}'.format(d['mounted_crystal_code']))
            ins = dal.mounted_crystals_table.insert().values(d)
            dal.connection.execute(ins)
            next += 1
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning('mounted crystal exists; skipping...')
            else:
                logger.error(str(e))
    pgbar.value = 0
    logger.info('finished inserting samples into mounted_crystals_table')

def update_soeked_crystal_table(logger, dal, soak_list, pgbar):
    logger.info('updating soaked crystals table in database')
    start, step = misc.get_step_for_progress_bar(len(soak_list))
    for d in soak_list:
        start += step
        pgbar.value = int(start)
        try:
            u = dal.soaked_crystals_table.update().values(d).where(
                dal.soaked_crystals_table.c.marked_crystal_code == d['marked_crystal_code'])
            dal.connection.execute(u)
        except Exception as e:
            logger.error(str(e))
    pgbar.value = 0
    logger.info('finished updating soaked_crystals_table')

def get_mounted_crystals_from_db_for_table_as_df(logger, dal):
    logger.info('reading mounted crystals from database')
    if dal.conn_string is not None:
        q = select([dal.mounted_crystals_table.c.mounted_crystal_code,
                    dal.mounted_crystals_table.c.puck_name,
                    dal.mounted_crystals_table.c.puck_position,
                    dal.mounted_crystals_table.c.shipment]).order_by(
                    dal.mounted_crystals_table.c.mounted_crystal_code.asc())
        df = pd.read_sql_query(q, dal.engine)
    else:
        logger.info('database not initialised; using blank values...')
        header = ['mounted_crystal_code', 'puck_name', 'puck_position', 'shipment']
        data = []
        for i in range(10):
            row = []
            for j in range(len(header)):
                row.append("............")
            data.append(row)
        df = pd.DataFrame(data, columns=[header])
    logger.info('finished reading mounted crystals from database')
    return df

def get_mounted_crystals_for_exi_where_shipment_is_none(logger, dal):
    logger.info('reading mounted crystals from database where shipment is none')
    q = select([dal.mounted_crystals_table.c.puck_name,
                dal.mounted_crystals_table.c.puck_position,
                dal.mounted_crystals_table.c.mounted_crystal_code]).where(
        dal.mounted_crystals_table.c.shipment == None).order_by(
        dal.mounted_crystals_table.c.mounted_crystal_code.asc())
    df = pd.read_sql_query(q, dal.engine)
    logger.info('found {0!s} number of crystals'.format(df.shape[0]))
    df = df.astype({'puck_position': 'int'})    # otherwise it could be 1.0
    df.insert(0, 'dewar', 'Dewar1')
    df.insert(2, 'type', 'Unipuck')
    df['sample'] = [x.split('-')[-1] for x in df['mounted_crystal_code']]
    df['mounted_crystal_code'] = [x.split('-')[-0] for x in df['mounted_crystal_code']]
    return df

def update_db_with_shipment_information(logger, dal, shipment):
    logger.info('updating mounted_crystal table with shipment information')
    u = dal.mounted_crystals_table.update().values(shipment=shipment).where(
        dal.mounted_crystals_table.c.shipment == None)
    dal.connection.execute(u)
    logger.info('finished updating mounted_crystal table with shipment information')

def get_joins(dal):
    k = dal.soaked_crystals_table.join(
        dal.marked_crystals_table, dal.soaked_crystals_table.c.marked_crystal_id ==
                                   dal.marked_crystals_table.c.marked_crystal_id, isouter=True).join(
        dal.mounted_crystals_table, dal.marked_crystals_table.c.marked_crystal_id ==
                                    dal.mounted_crystals_table.c.marked_crystal_id, isouter=True).join(
        dal.xray_dataset_table, dal.mounted_crystals_table.c.mounted_crystal_id ==
                                dal.xray_dataset_table.c.mounted_crystal_id, isouter=True).join(
        dal.xray_processing_table, dal.xray_dataset_table.c.dataset_id ==
                                   dal.xray_processing_table.c.dataset_id, isouter=True).join(
        dal.xray_initial_refinement_table, dal.xray_processing_table.c.processing_id ==
                                           dal.xray_initial_refinement_table.c.processing_id, isouter=True).join(
        dal.soak_plate_table, dal.soaked_crystals_table.c.soak_plate_id ==
                              dal.soak_plate_table.c.soak_plate_id, isouter=True).join(
        dal.compound_batch_table, dal.soak_plate_table.c.compound_batch_code ==
                                  dal.compound_batch_table.c.compound_batch_code, isouter=True).join(
        dal.compound_table, dal.compound_batch_table.c.compound_code ==
                            dal.compound_table.c.compound_code, isouter=True).join(
        dal.crystal_screen_condition_table, dal.marked_crystals_table.c.crystal_screen_condition_id ==
                                            dal.crystal_screen_condition_table.c.crystal_screen_condition_id,
        isouter=True).join(
        dal.crystal_plate_table, dal.marked_crystals_table.c.crystal_plate_id ==
                                 dal.crystal_plate_table.c.crystal_plate_id, isouter=True).join(
        dal.protein_batch_table, dal.crystal_plate_table.c.protein_batch_id ==
                                 dal.protein_batch_table.c.protein_batch_id, isouter=True)
    return k


def get_summary_dataframe(logger, dal):
    logger.info('reading mounted crystals summary from database')
    k = get_joins(dal)

    q = select([dal.mounted_crystals_table.c.mounted_crystal_code,
                dal.protein_batch_table.c.protein_batch_name,
                dal.marked_crystals_table.c.crystal_plate_barcode,
                dal.marked_crystals_table.c.crystal_plate_well,
                dal.compound_table.c.compound_code,
                dal.compound_batch_table.c.library_name,

                dal.compound_batch_table.c.compound_plate_name,
                dal.compound_batch_table.c.compound_plate_well,

                dal.mounted_crystals_table.c.puck_name,
                dal.mounted_crystals_table.c.puck_position,


                dal.compound_table.c.smiles,
                dal.compound_table.c.vendor_id,
                dal.compound_table.c.vendor,
                dal.mounted_crystals_table.c.mount_datetime,
                dal.soaked_crystals_table.c.soak_datetime,
                dal.crystal_screen_condition_table.c.crystal_screen_condition,
                dal.mounted_crystals_table.c.manual_mounted_crystal_code,
                dal.compound_table.c.compound_code,
                dal.soaked_crystals_table.c.compound_appearance,
                dal.soaked_crystals_table.c.crystal_appearance,
                dal.soaked_crystals_table.c.soak_datetime,
                dal.xray_dataset_table.c.data_collection_date,
                dal.xray_dataset_table.c.data_collection_outcome,
                dal.xray_dataset_table.c.is_dataset,
                dal.xray_dataset_table.c.selected.label('xray_dataset_table_selected'),
                dal.xray_processing_table.c.selected.label('xray_processing_table_selected'),
                dal.xray_processing_table.c.autoproc_pipeline,
                dal.xray_processing_table.c.sym_space_group,
                dal.xray_processing_table.c.reflns_d_resolution_high,
                dal.xray_processing_table.c.reflns_inner_pdbx_Rmerge_I_obs,
                dal.xray_processing_table.c.reflns_outer_pdbx_netI_over_sigmaI,
                dal.xray_initial_refinement_table.c.refinement_software,
                dal.xray_initial_refinement_table.c.sym_space_group,
                dal.xray_initial_refinement_table.c.refine_ls_R_factor_R_work,
                dal.xray_initial_refinement_table.c.refine_ls_R_factor_R_free,
                dal.xray_initial_refinement_table.c.refine_r_bond_refined_d,
                dal.xray_initial_refinement_table.c.refine_r_angle_refined_deg,
                dal.xray_initial_refinement_table.c.selected.label('xray_initial_refinement_table_table')
                ]).order_by(dal.mounted_crystals_table.c.mounted_crystal_code.asc())
#    q = q.select_from(j)
#    q = q.select_from(i)
#    q = q.select_from(i)
    q = q.select_from(k)
    df = pd.read_sql_query(q, dal.engine)
#    df['soak_time'] = (df.mount_datetime - df.soak_datetime)
    df['preparation_date'] = df['soak_datetime'].dt.date
    df.insert(4, 'soak_time', (df.mount_datetime - df.soak_datetime).astype('timedelta64[h]'))
#    df['soak_time'] = df['soak_time'].

    df.loc[df["mounted_crystal_code"] == "", "mounted_crystal_code"] = "xtal died during soak"

    df = df.drop('mount_datetime', axis=1)
    df = df.drop('soak_datetime', axis=1)
    df = df[df["is_dataset"] != False]

    df = df[df["xray_dataset_table_selected"] != False]
    df = df[df["xray_processing_table_selected"] != False]
    df = df[df["xray_initial_refinement_table_table"] != False]

#    df = df[df["selected"] != False]
#    df = df[df["selected_1"] != False]
#    df = df.drop('is_dataset', axis=1)
#    df = df.drop('selected', axis=1)
#    df = df.drop('selected_1', axis=1)

    df = df.drop('xray_dataset_table_selected', axis=1)
    df = df.drop('xray_processing_table_selected', axis=1)
    df = df.drop('xray_initial_refinement_table_table', axis=1)

#    df = df.drop_duplicates(subset=['mounted_crystal_code'], keep='last')

#    df = df[['mounted_crystal_code', 'compound_code', 'smiles', 'vendor_id', 'vendor', 'soak_time',
#             'crystal_screen_condition']]
    logger.info('finished reading mounted crystals summary from database')
    return df

def get_fragmax_dataframe(logger, dal):
    logger.info('reading mounted crystals for fragmaxapp csv file from database')
    k = get_joins(dal)
    q = select([dal.mounted_crystals_table.c.mounted_crystal_code,
                dal.compound_batch_table.c.library_name,
                dal.compound_batch_table.c.compound_code]).order_by(
                dal.mounted_crystals_table.c.mounted_crystal_code.asc())
    q = q.select_from(k)
    df = pd.read_sql_query(q, dal.engine)
    return df