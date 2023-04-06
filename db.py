from datetime import datetime
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
        DateTime, ForeignKey, Boolean, create_engine, UniqueConstraint)

class DataAccessLayer:
    connection = None
    engine = None
    conn_string = None
    metadata = MetaData()

    """
    class generates all tables in database
    """

    project_table = Table('project_table',
        metadata,
        Column('project_id', Integer(), primary_key=True),
        Column('project_name', String(255), index=True),
        Column('proposal_number', String(50)),
        Column('project_description', String(255)),
        Column('project_directory', String(255)),
        Column('protein_acronym', String(50), unique=True),
        Column('protein_name', String(255)),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('protein_acronym', name='unique_protein_acronym')
    )

    protein_batch_table = Table('protein_batch_table',
        metadata,
        Column('protein_batch_id', Integer(), primary_key=True),
        Column('protein_batch_name', String(255)),
        Column('protein_acronym', String(50), ForeignKey('project_table.protein_acronym')),
        Column('protein_batch_supplier_name', String(255)),
        Column('protein_batch_sequence', String(2550)),
        Column('protein_batch_expression_host', String(255)),
        Column('protein_batch_buffer', String(255)),
        Column('protein_batch_concentration', Numeric(12, 2)),
        Column('protein_batch_concentration_unit_id', ForeignKey('unit_table.unit_id')),
        Column('protein_batch_date_received', DateTime(), default=datetime.now),
        Column('protein_batch_comment', String(2550)),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('protein_batch_name', name='unique_protein_batch_name')
    )

    crystal_screen_table = Table('crystal_screen_table',
        metadata,
        Column('crystal_screen_id', Integer(), primary_key=True),
        Column('crystal_screen_name', String(50), index=True),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('crystal_screen_name', name='unique_idx')
    )

    crystal_screen_condition_table = Table('crystal_screen_condition_table',
        metadata,
        Column('crystal_screen_condition_id', Integer(), primary_key=True),
        Column('crystal_screen_id', ForeignKey('crystal_screen_table.crystal_screen_id')),
        Column('crystal_screen_condition', String(255)),
        Column('crystal_screen_well', String(12)),
        Column('crystal_screen_row', String(12)),
        Column('crystal_screen_column', String(12)),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('crystal_screen_id', 'crystal_screen_row', 'crystal_screen_column', name='unique_idx')
    )

    crystal_plate_table = Table('crystal_plate_table',
        metadata,
        Column('crystal_plate_id', Integer(), primary_key=True),
        Column('crystal_plate_barcode', String(255), index=True),
        Column('protein_batch_id', ForeignKey('protein_batch_table.protein_batch_id')),
        Column('protein_batch_concentration', Numeric(12, 2)),
        Column('protein_batch_concentration_unit_id', ForeignKey('unit_table.unit_id')),
        Column('protein_batch_buffer', String(255)),
        Column('protein_history', String(255)),
        Column('comment', String(255)),
        Column('crystal_screen_id', ForeignKey('crystal_screen_table.crystal_screen_id')),
        Column('method_id', ForeignKey('crystallization_method_table.method_id')),
        Column('temperature', Numeric(12, 2)),
        Column('plate_type_id', ForeignKey('plate_type_table.plate_type_id')),
        Column('reservoir_volume', Numeric(12, 2)),
        Column('reservoir_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('start_row', String(8)),
        Column('end_row', String(8)),
        Column('start_column', String(8)),
        Column('end_column', String(8)),
        Column('subwell_01_protein_volume', Numeric(12, 2)),
        Column('subwell_01_protein_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_01_reservoir_volume', Numeric(12, 2)),
        Column('subwell_01_reservoir_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_01_seed_volume', Numeric(12, 2)),
        Column('subwell_01_seed_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_00_protein_volume', Numeric(12, 2)),
        Column('subwell_00_protein_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_00_reservoir_volume', Numeric(12, 2)),
        Column('subwell_00_reservoir_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_00_seed_volume', Numeric(12, 2)),
        Column('subwell_00_seed_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_02_protein_volume', Numeric(12, 2)),
        Column('subwell_02_protein_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_02_reservoir_volume', Numeric(12, 2)),
        Column('subwell_02_reservoir_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_02_seed_volume', Numeric(12, 2)),
        Column('subwell_02_seed_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_03_protein_volume', Numeric(12, 2)),
        Column('subwell_03_protein_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_03_reservoir_volume', Numeric(12, 2)),
        Column('subwell_03_reservoir_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('subwell_03_seed_volume', Numeric(12, 2)),
        Column('subwell_03_seed_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('crystal_plate_barcode', name='unique_crystal_plate_barcode')
    )

    marked_crystals_table = Table('marked_crystals_table',
        metadata,
        Column('marked_crystal_id', Integer(), primary_key=True),
        Column('marked_crystal_code', String(255), index=True),
        Column('crystal_plate_id', ForeignKey('crystal_plate_table.crystal_plate_id')),
        Column('crystal_screen_condition_id', ForeignKey('crystal_screen_condition_table.crystal_screen_condition_id')),
        Column('crystal_plate_barcode', String(55)),
        Column('crystal_plate_row', String(55)),
        Column('crystal_plate_column', String(55)),
        Column('crystal_plate_subwell', String(55)),
        Column('crystal_plate_well', String(55)),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('marked_crystal_code', name='unique_marked_crystal_code')
    )

    soak_plate_table = Table('soak_plate_table',
        metadata,
        Column('soak_plate_id', Integer(), primary_key=True),
        Column('soak_plate_name', String(55)),
        Column('compound_batch_code', ForeignKey('compound_batch_table.compound_batch_code')),
        Column('compound_plate_name', String(55)),
        Column('soak_plate_type', String(20)),
        Column('soak_plate_type_id', ForeignKey('plate_type_table.plate_type_id')),
        Column('soak_plate_row', String(55)),
        Column('soak_plate_column', String(55)),
        Column('soak_plate_well', String(55)),
        Column('soak_plate_subwell', String(55)),
        Column('base_buffer', String(55)),
        Column('base_buffer_volume', Numeric(12, 2)),
        Column('base_buffer_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('compound_volume', Numeric(12, 2)),
        Column('compound_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('soak_plate_name', 'soak_plate_well', name='unique_name_well')
    )

    soaked_crystals_table = Table('soaked_crystals_table',
        metadata,
        Column('soaked_crystals_id', Integer(), primary_key=True),
        Column('soak_plate_name', String(55)),
        Column('soak_plate_id', ForeignKey('soak_plate_table.soak_plate_id')),
        Column('marked_crystal_code', String(255)),
        Column('marked_crystal_id', ForeignKey('marked_crystals_table.marked_crystal_id')),
        Column('compound_appearance', String(50)),
        Column('crystal_appearance', String(50)),
        Column('status', String(50)),   # soak_success, soak_fail, mount_success, mount_fail
        Column('soak_plate_type', String(20)),
        Column('soak_plate_well', String(55)),
        Column('soak_solution_volume', Numeric(12, 2)),
        Column('soak_solution_volume_unit', String(8)),
        Column('soak_solution_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('soak_method', String(55)),
        Column('soak_temperature', Numeric(12, 2)),
        Column('soak_temperature_unit_id', ForeignKey('unit_table.unit_id')),
        Column('comment', String(255)),
        Column('soak_datetime', DateTime(), default=datetime.now),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('soak_datetime', 'marked_crystal_id', name='unique_soak_datetime_crystal_id')
    )

    mounted_crystals_table = Table('mounted_crystals_table',
        metadata,
        Column('mounted_crystal_id', Integer(), primary_key=True),
        Column('mounted_crystal_code', String(255), index=True),
        Column('pin_barcode', String(55)),
        Column('puck_name', String(55)),
        Column('puck_position', Integer()),
        Column('mount_datetime', DateTime(), default=datetime.now),
        Column('mount_temperature', Numeric(12, 2)),
        Column('mount_temperature_unit_id', ForeignKey('unit_table.unit_id')),
        Column('shipment', String(55)),
        Column('marked_crystal_code', String(255)),
        Column('marked_crystal_id', ForeignKey('marked_crystals_table.marked_crystal_id')),
        Column('compound_appearance', String(50)),
        Column('crystal_appearance', String(50)),
        Column('cryo', String(55)),
        Column('cryo_volume', Numeric(12, 2)),
        Column('cryo_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('manual_mounted_crystal_code', String(55)),
        Column('data_collection_comment', String(55)),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('mount_datetime', name='unique_mount_datetime')
    )

    compound_table = Table('compound_table',
        metadata,
        Column('compound_id', Integer(), primary_key=True),
        Column('compound_code', String(50), index=True, unique=True),
        Column('chemical_name', String(255)),
        Column('smiles', String(255)),
        Column('inchi', String(255)),
        Column('cas', String(255)),
        Column('vendor', String(55)),
        Column('vendor_id', String(55)),
        Column('plate_name', String(55)),
        Column('cocktail', Boolean(), default=False),
        Column('covalent', Boolean(), default=False),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('compound_code', name='unique_compound_code')
    )

    compound_batch_table = Table('compound_batch_table',
        metadata,
        Column('compound_batch_id', Integer(), primary_key=True),
        Column('compound_batch_code', String(50), index=True),
        Column('compound_code', ForeignKey('compound_table.compound_code')),
        Column('library_name', String(55)),
        Column('compound_plate_name', String(55)),
        Column('compound_plate_row', String(8)),
        Column('compound_plate_column', String(8)),
        Column('compound_plate_well', String(8)),
        Column('compound_plate_type', ForeignKey('plate_type_table.plate_type_id')),
        Column('solvent', ForeignKey('compound_table.compound_code')),
        Column('compound_concentration', Numeric(12, 2)),
        Column('compound_concentration_unit', String(50)),
        Column('compound_concentration_unit_id', ForeignKey('unit_table.unit_id')),
        Column('compound_volume', Numeric(12, 2)),
        Column('compound_volume_unit', String(50)),
        Column('compound_volume_unit_id', ForeignKey('unit_table.unit_id')),
        Column('comment', String(255)),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now),
        UniqueConstraint('compound_batch_code', name='unique_compound_batch_code')
    )




    unit_table = Table('unit_table',
        metadata,
        Column('unit_id', Integer(), primary_key=True),
        Column('unit_symbol', String(50), index=True),
        Column('unit_name', String(50)),
        Column('conversion_factor', Numeric(12, 12)),
        Column('type', String(50)),
        UniqueConstraint('unit_symbol', name='unique_unit_symbol')
    )

    plate_type_table = Table('plate_type_table',
        metadata,
        Column('plate_type_id', Integer(), primary_key=True),
        Column('plate_type_name', String(20), index=True),
        UniqueConstraint('plate_type_name', name='unique_plate_type_name')
    )

    crystallization_method_table = Table('crystallization_method_table',
        metadata,
        Column('method_id', Integer(), primary_key=True),
        Column('method_name', String(50), index=True),
        UniqueConstraint('method_name', name='unique_method_name')
    )

    soak_method_table = Table('soak_method_table',
        metadata,
        Column('method_id', Integer(), primary_key=True),
        Column('method_name', String(50), index=True),
        UniqueConstraint('method_name', name='unique_method_name')
    )

    space_group_table = Table('space_group_table',
        metadata,
        Column('space_group_id', Integer(), primary_key=True),
        Column('space_group_name', String(50), index=True),
        Column('space_group_number', Integer()),
        UniqueConstraint('space_group_name', name='unique_space_group_name')
    )

    def db_init(self, conn_string):
        self.engine = create_engine('sqlite:///' + conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

dal = DataAccessLayer()
