-- version "00001" - start

ALTER TABLE project_table ADD 'external_url' VARCHAR;

ALTER TABLE protein_batch_table ADD 'protein_batch_uniprot_id'  VARCHAR;
ALTER TABLE protein_batch_table ADD 'protein_batch_comp_id'   VARCHAR;
ALTER TABLE protein_batch_table ADD 'protein_batch_source_organism'  VARCHAR;
ALTER TABLE protein_batch_table ADD 'protein_batch_vector'  VARCHAR;

ALTER TABLE compound_table ADD 'chem_comp_code'  VARCHAR;
ALTER TABLE compound_table ADD 'chem_comp_id' VARCHAR;
ALTER TABLE compound_table ADD 'formula'   VARCHAR;
ALTER TABLE compound_table ADD 'formula_weight'    NUMERIC(12,2);

ALTER TABLE compound_batch_table ADD 'compound_batch_active'    BOOLEAN;
ALTER TABLE compound_batch_table ADD 'solvent_chem_comp_code'     VARCHAR;

ALTER TABLE marked_crystals_table ADD "marked_crystal_image"  VARCHAR;

ALTER TABLE mounted_crystals_table ADD 'cryo_chem_comp_code'      VARCHAR;

ALTER TABLE xray_processing_table ADD 'data_reduction_software_version'  VARCHAR;
ALTER TABLE xray_processing_table ADD 'data_scaling_software_version'  VARCHAR;
ALTER TABLE xray_processing_table ADD 'autoproc_pipeline_version'  VARCHAR;
ALTER TABLE xray_processing_table ADD 'resolution_high_1_0_sigma'  VARCHAR;
ALTER TABLE xray_processing_table ADD 'resolution_high_1_5_sigma'  VARCHAR;
ALTER TABLE xray_processing_table ADD 'resolution_high_2_0_sigma'  VARCHAR;
ALTER TABLE xray_processing_table ADD 'staraniso_version'  VARCHAR;
ALTER TABLE xray_processing_table ADD "selected"  BOOLEAN;
ALTER TABLE xray_processing_table ADD 'processing_outcome'  VARCHAR;

ALTER TABLE xray_dataset_table ADD "detector_distance"  NUMERIC(12,2);
ALTER TABLE xray_dataset_table ADD "omega_range_total"  NUMERIC(12,2);
ALTER TABLE xray_dataset_table ADD "n_images"  NUMERIC(12,2);
ALTER TABLE xray_dataset_table ADD "is_dataset"  INTERGER;
ALTER TABLE xray_dataset_table ADD "data_collection_type"  VARCHAR;

ALTER TABLE xray_initial_refinement_table ADD "selected"  BOOLEAN;
ALTER TABLE xray_initial_refinement_table ADD "refinement_software_version"  VARCHAR;
ALTER TABLE xray_initial_refinement_table ADD "input_mtz_file"  VARCHAR;
ALTER TABLE xray_initial_refinement_table ADD "input_mtz_free_file"  VARCHAR;
ALTER TABLE xray_initial_refinement_table ADD "initial_refinement_outcome"  VARCHAR;

CREATE TABLE version_table (
	version_id INTEGER NOT NULL,
	version_number VARCHAR,
	created_on DATETIME,
	updated_on DATETIME,
	PRIMARY KEY (version_id),
	CONSTRAINT version_number UNIQUE (version_number)
)
-- version "00001" - end -----------------------------------------

