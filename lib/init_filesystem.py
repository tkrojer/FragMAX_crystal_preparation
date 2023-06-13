from shutil import (copyfile, move)
from datetime import datetime
import os

import log

class init_filesystem(object):
    def __init__(self, settingsObject, logger):
        self.settings = settingsObject
        self.logger = logger

    def init_folders(self):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.settings.logfile_folder = os.path.join(self.settings.project_folder, 'log')
        if not os.path.isdir(self.settings.logfile_folder):
            os.mkdir(self.settings.logfile_folder)
            os.mkdir(os.path.join(self.settings.logfile_folder, 'backup'))
        logfile = os.path.join(self.settings.logfile_folder, 'logfile.log')
        if os.path.isfile(logfile):
            move(logfile, os.path.join(os.path.join(self.settings.logfile_folder, 'backup', 'logfile.log.' + now)))
        self.logger = log.init_logger(self.logger, os.path.join(self.settings.logfile_folder, 'logfile.log'))
        self.logger.info('starting new session...')

        self.settings.db_dir = os.path.join(self.settings.project_folder, 'database')
        if os.path.isdir(self.settings.db_dir):
            self.logger.warning('DB folder exists: ' + self.settings.db_dir)
        else:
            self.logger.info('creating DB folder: ' + self.settings.db_dir)
            os.mkdir(self.settings.db_dir)
            os.mkdir(os.path.join(self.settings.db_dir, 'backup'))

        self.settings.crystal_image_folder = os.path.join(self.settings.project_folder, 'crystal_images')
        if os.path.isdir(self.settings.crystal_image_folder):
            self.logger.warning('crystal image folder exists: ' + self.settings.crystal_image_folder)
        else:
            self.logger.info('creating crystal image folder: ' + self.settings.crystal_image_folder)
            os.mkdir(self.settings.crystal_image_folder)

        self.settings.crystal_screen_folder = os.path.join(self.settings.project_folder, 'crystal_screen')
        if os.path.isdir(self.settings.crystal_screen_folder):
            self.logger.warning('crystal screen folder exists: ' + self.settings.crystal_screen_folder)
        else:
            self.logger.info('creating screen image folder: ' + self.settings.crystal_screen_folder)
            os.mkdir(self.settings.crystal_screen_folder)

        self.settings.workflow_folder = os.path.join(self.settings.project_folder, 'workflow')
        if os.path.isdir(self.settings.workflow_folder):
            self.logger.warning('workflow folder exists: ' + self.settings.workflow_folder)
        else:
            self.logger.info('creating workflow folder: ' + self.settings.workflow_folder)
            os.mkdir(self.settings.workflow_folder)

        workflow_inspect_folder = os.path.join(self.settings.project_folder, 'workflow', '1-inspect')
        if os.path.isdir(workflow_inspect_folder):
            self.logger.warning('workflow/1-inspect folder exists: ' + workflow_inspect_folder)
        else:
            self.logger.info('creating workflow/1-inspect folder: ' + workflow_inspect_folder)
            os.mkdir(workflow_inspect_folder)
            os.mkdir(os.path.join(workflow_inspect_folder, 'backup'))

        workflow_soak_folder = os.path.join(self.settings.project_folder, 'workflow', '2-soak')
        if os.path.isdir(workflow_soak_folder):
            self.logger.warning('workflow/2-soak folder exists: ' + workflow_soak_folder)
        else:
            self.logger.info('creating workflow/2-soak folder: ' + workflow_soak_folder)
            os.mkdir(workflow_soak_folder)
            os.mkdir(os.path.join(workflow_soak_folder, 'backup'))

        workflow_mount_folder = os.path.join(self.settings.project_folder, 'workflow', '3-mount')
        if os.path.isdir(workflow_mount_folder):
            self.logger.warning('workflow/3-mount folder exists: ' + workflow_mount_folder)
        else:
            self.logger.info('creating workflow/3-mount folder: ' + workflow_mount_folder)
            os.mkdir(workflow_mount_folder)
            os.mkdir(os.path.join(workflow_mount_folder, 'backup'))

        workflow_mount_manual_folder = os.path.join(self.settings.project_folder, 'workflow', '4-mount-manual')
        if os.path.isdir(workflow_mount_manual_folder):
            self.logger.warning('workflow/4-mount-manual folder exists: ' + workflow_mount_manual_folder)
        else:
            self.logger.info('creating workflow/4-mount-manual folder: ' + workflow_mount_manual_folder)
            os.mkdir(workflow_mount_manual_folder)
            os.mkdir(os.path.join(workflow_mount_manual_folder, 'backup'))

        workflow_exi_folder = os.path.join(self.settings.project_folder, 'workflow', '5-exi')
        if os.path.isdir(workflow_exi_folder):
            self.logger.warning('workflow/5-exi folder exists: ' + workflow_exi_folder)
        else:
            self.logger.info('creating workflow/5-exi folder: ' + workflow_exi_folder)
            os.mkdir(workflow_exi_folder)
            os.mkdir(os.path.join(workflow_exi_folder, 'backup'))

        workflow_fragmaxapp_folder = os.path.join(self.settings.project_folder, 'workflow', '6-fragmaxapp')
        if os.path.isdir(workflow_fragmaxapp_folder):
            self.logger.warning('workflow/6-fragmaxapp folder exists: ' + workflow_fragmaxapp_folder)
        else:
            self.logger.info('creating workflow/6-fragmaxapp folder: ' + workflow_fragmaxapp_folder)
            os.mkdir(workflow_fragmaxapp_folder)
            os.mkdir(os.path.join(workflow_fragmaxapp_folder, 'backup'))

        workflow_summary_folder = os.path.join(self.settings.project_folder, 'workflow', '7-summary')
        if os.path.isdir(workflow_summary_folder):
            self.logger.warning('workflow/7-summary folder exists: ' + workflow_summary_folder)
        else:
            self.logger.info('creating workflow/7-summary folder: ' + workflow_summary_folder)
            os.mkdir(workflow_summary_folder)

        workflow_inspect_manual_folder = os.path.join(self.settings.project_folder, 'workflow', '8-inspect-manual')
        if os.path.isdir(workflow_inspect_manual_folder):
            self.logger.warning('workflow/8-inspect-manual folder exists: ' + workflow_inspect_manual_folder)
        else:
            self.logger.info('creating workflow/8-inspect-manual folder: ' + workflow_inspect_manual_folder)
            os.mkdir(workflow_inspect_manual_folder)

        self.settings.eln_folder = os.path.join(self.settings.project_folder, 'eln')
        if os.path.isdir(self.settings.eln_folder):
            self.logger.warning('eln folder exists: ' + self.settings.eln_folder)
        else:
            self.logger.info('eln image folder: ' + self.settings.eln_folder)
            os.mkdir(self.settings.eln_folder)

    def init_db(self, dal):
        self.settings.db_file = os.path.join(self.settings.db_dir, 'fragmax.sqlite')
        self.logger.info("checking if database exists in {0!s}".format(self.settings.db_file))
        if os.path.isfile(str(self.settings.db_file)):
            self.logger.info("found database file")
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.logger.info('creating backup current DB file: ' + os.path.join(self.settings.db_dir,
                                                                                'backup', 'fragmax.sqlite.' + now))
            copyfile(self.settings.db_file, os.path.join(self.settings.db_dir, 'backup', 'fragmax.sqlite.' + now))
        else:
            self.logger.warning("cannot find database file; this is probably a new session")
        self.logger.info('initializing database')
        dal.db_init(self.settings.db_file)
