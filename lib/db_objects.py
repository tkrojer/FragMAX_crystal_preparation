class db_objects(object):
    def __init__(self):
        self.connection = None
        self.engine = None

        self.projectTable = None
        self.crystalscreenTable = None
        self.proteinTable = None
        self.proteinBatchTable = None
        self.crystal_plate_typeTable = None
        self.crystalplateTable = None
        self.markedcrystalTable = None
        self.soakplateTable = None
        self.compoundbatchTable = None
        self.soakedcrystalTable = None
        self.mountedcrystalTable = None
        self.diaryTable = None

