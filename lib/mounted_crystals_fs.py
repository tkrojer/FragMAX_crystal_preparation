import os
import pandas as pd

import sys
sys.path.append(os.path.join(os.getcwd(), 'lib'))
import misc

def get_shifter_csv_file_as_dict_list(logger, shifter_csv_file):
    xtal_list = []
    soak_list = []
    for line in open(shifter_csv_file, encoding='utf-8-sig'):
        mount_dict, soak_dict = misc.read_line_from_shifter_csv_as_mounted_crystal_dict(logger, line)
        if mount_dict:
            xtal_list.append(mount_dict)
        if soak_dict:
            soak_list.append(soak_dict)
    return xtal_list, soak_list
