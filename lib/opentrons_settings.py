class settings(object):
    def __init__(self):
        self.project_folder = None
        self.workflow_folder = None
        self.logfile_folder = None
        self.opentrons_ready = False
#        self.plate_dict = {'crystal_plate': [], 'soak_plate': []}
        self.rack_dict = {
            '01': None,
            '02': None,
            '03': None,
            '04': None,
            '05': None,
            '06': None,
            '07': None,
            '08': None,
            '09': None,
            '10': None,
            '11': None
        }
        self.plate_types = [
            'target',
            'compound 1',
            'compound 2',
            'tip_rack 1',
            'tip_rack 2'
        ]


