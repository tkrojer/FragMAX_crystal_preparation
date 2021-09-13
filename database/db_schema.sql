CREATE TABLE IF NOT EXISTS "Project" (
	"Project_Name"	TEXT,
	"Proposal_ID"	TEXT,
	"Project_Description"	TEXT,
	"Project_Directory"     TEXT
);
CREATE TABLE IF NOT EXISTS "People" (
	"Forename"	TEXT,
	"Surname"	TEXT,
	"Email"	TEXT,
	"Role"	TEXT,
	"ORCID"	TEXT,
	"Organization_Name"	TEXT,
	"Street"	TEXT,
	"City"	TEXT,
	"ZIP_Code"	TEXT,
	"Country"	TEXT,
	"Phone"	TEXT
);
CREATE TABLE IF NOT EXISTS "CrystalPlateType" (
	"Plate_Name"	TEXT
);

CREATE TABLE IF NOT EXISTS "Protein" (
	"Protein_Name"	TEXT,
	"Protein_Acronym"	TEXT,
	"Organsism"	TEXT,
	"Expression_Host"	TEXT,
	"Sequence"	TEXT,
	PRIMARY KEY("Protein_Acronym")
);
CREATE TABLE IF NOT EXISTS "CompoundTable" (
	"Compound_ID"	TEXT,
	"Compound_Name"	TEXT,
	"Vendor_ID"	TEXT,
	"Vendor"	TEXT,
	"Smiles"	TEXT,
	"InChI"	TEXT,
	"CAS"	TEXT,
	"Cocktail"  TEXT,
	"Covalent"  TEXT,
	PRIMARY KEY("Compound_ID")
);
CREATE TABLE IF NOT EXISTS "CompoundBatchTable" (
	"CompoundBatch_ID"	TEXT,
	"Compound_ID"	TEXT,
	"Library_Name"	TEXT,
	"CompoundPlate_Name"    TEXT,
	"CompoundPlate_Well" TEXT,
	"CompoundPlate_Type" TEXT,
	"State"	TEXT,
	"Solvent"	TEXT,
	"Concentration"	REAL,
	"Comment"	TEXT,
	PRIMARY KEY("CompoundBatch_ID")
);
CREATE TABLE IF NOT EXISTS "MountedCrystals" (
	"Crystal_ID"	TEXT,
	"Pin_Barcode"	TEXT,
	"Puck_Name"	TEXT,
	"Puck_Position"	TEXT,
	"Mount_Date"	TEXT,
	"SoakPlate_Condition_ID"	TEXT,
	"MarkedCrystal_ID"	TEXT,
	"Cryo"      TEXT,
	"Cryo_Concentration"    TEXT,
	"CompoundBatch_ID"  TEXT,
	"Comment"   TEXT,
	"Shipment"  TEXT,
	"Manual_Crystal_ID" TEXT,
	PRIMARY KEY("Crystal_ID")
);
CREATE TABLE IF NOT EXISTS "CrystalForm" (
	"Crystal_Form"	TEXT,
	"Protein_Acronym"	TEXT,
	"Space_Group"	TEXT,
	"A"	REAL,
	"B"	REAL,
	"C"	REAL,
	"Alpha"	REAL,
	"Beta"	REAL,
	"Gamma"	REAL,
	PRIMARY KEY("Crystal_Form")
);
CREATE TABLE IF NOT EXISTS "SpaceGroupTable" (
	"SpaceGroup_Name"	TEXT,
	"SpaceGroup_Number"	INTEGER
);
CREATE TABLE IF NOT EXISTS "MarkedCrystals" (
	"MarkedCrystal_ID"	TEXT,
	"CrystalPlate_Barcode"	TEXT,
	"CrystalPlate_Well"	TEXT,
	"CrystalPlate_Subwell"	TEXT,
	PRIMARY KEY("MarkedCrystal_ID")
);
CREATE TABLE IF NOT EXISTS "SoakPlate" (
	"SoakPlate_Condition_ID"	TEXT,
	"SoakPlate_Name"	TEXT,
	"SoakPlate_Well"	TEXT,
	"SoakPlate_Subwell"	TEXT,
	"CompoundPlate_Name"    TEXT,
	"CompoundBatch_ID"	TEXT,
	"Plate_Type"	TEXT,
	"CrystalBuffer"	TEXT,
	"CrystalBuffer_Vol"	REAL,
	"Compound_Vol"	REAL,
	PRIMARY KEY("SoakPlate_Condition_ID")
);
CREATE TABLE IF NOT EXISTS "SoakedCrystals" (
	"Soak_ID"	TEXT,
	"MarkedCrystal_ID"	TEXT,
	"SoakPlate_Condition_ID"	TEXT,
	"Soak_Time"	TEXT,
	"Soak_Comment"	TEXT,
	PRIMARY KEY("Soak_ID")
);
CREATE TABLE IF NOT EXISTS "CrystalScreen" (
	"CrystalScreen_ID"	TEXT,
	"CrystalScreen_Name"	TEXT,
	"CrystalScreen_Well"	TEXT,
	"CrystalScreen_Condition"	TEXT,
	PRIMARY KEY("CrystalScreen_ID")
);
CREATE TABLE IF NOT EXISTS "CrystalPlate" (
	"CrystalPlate_Barcode"	TEXT,
	"Protein_Acronym"	TEXT,
	"Protein_Concentration"	REAL,
	"CrystalScreen_Name"	TEXT,
	"Compound1Batch_ID" TEXT,
	"Compound1_Volume"  REAL,
	"Compound2Batch_ID" TEXT,
	"Compound2_Volume"  REAL,
	"Compound3Batch_ID" TEXT,
	"Compound3_Volume"  REAL,
	"Protein_Buffer"	TEXT,
	"Temperature"	REAL,
	"Plate_Type"	TEXT,
	"Reservoir_Volume"	REAL,
	"Subwell_A_Vol_Protein"	REAL,
	"Subwell_A_Vol_Reservoir"	REAL,
	"Subwell_A_Vol_Seed"	REAL,
	"Subwell_C_Vol_Protein"	REAL,
	"Subwell_C_Vol_Reservoir"	REAL,
	"Subwell_C_Vol_Seed"	REAL,
	"Subwell_D_Vol_Protein"	REAL,
	"Subwell_D_Vol_Reservoir"	REAL,
	"Subwell_D_Vol_Seed"	REAL,
	PRIMARY KEY("CrystalPlate_barcode")
);
INSERT INTO CrystalPlateType VALUES('SwissCI-MRC-3d');
COMMIT;

