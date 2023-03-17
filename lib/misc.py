import os
from datetime import datetime
from shutil import (copyfile, move)
import re

def swiss_ci_3_drop_layout():

    coordinates = [
        ['A01a', 1, 24, 'circle',     'A', '01', '01', '01'],
        ['A01b', 2, 24, 'rectangle',  'A', '01', '01', '00'],
        ['A01c', 1, 23, 'circle',     'A', '01', '01', '02'],
        ['A01d', 2, 23, 'circle',     'A', '01', '01', '03'],
        ['A02a', 4, 24, 'circle',     'A', '01', '02', '01'],
        ['A02b', 5, 24, 'rectangle',  'A', '01', '02', '00'],
        ['A02c', 4, 23, 'circle',     'A', '01', '02', '02'],
        ['A02d', 5, 23, 'circle',     'A', '01', '02', '03'],
        ['A03a', 7, 24, 'circle',     'A', '01', '03', '01'],
        ['A03b', 8, 24, 'rectangle',  'A', '01', '03', '00'],
        ['A03c', 7, 23, 'circle',     'A', '01', '03', '02'],
        ['A03d', 8, 23, 'circle',     'A', '01', '03', '03'],
        ['A04a', 10, 24, 'circle',    'A', '01', '04', '01'],
        ['A04b', 11, 24, 'rectangle', 'A', '01', '04', '00'],
        ['A04c', 10, 23, 'circle',    'A', '01', '04', '02'],
        ['A04d', 11, 23, 'circle',    'A', '01', '04', '03'],
        ['A05a', 13, 24, 'circle',    'A', '01', '05', '01'],
        ['A05b', 14, 24, 'rectangle', 'A', '01', '05', '00'],
        ['A05c', 13, 23, 'circle',    'A', '01', '05', '02'],
        ['A05d', 14, 23, 'circle',    'A', '01', '05', '03'],
        ['A06a', 16, 24, 'circle',    'A', '01', '06', '01'],
        ['A06b', 17, 24, 'rectangle', 'A', '01', '06', '00'],
        ['A06c', 16, 23, 'circle',    'A', '01', '06', '02'],
        ['A06d', 17, 23, 'circle',    'A', '01', '06', '03'],
        ['A07a', 19, 24, 'circle',    'A', '01', '07', '01'],
        ['A07b', 20, 24, 'rectangle', 'A', '01', '07', '00'],
        ['A07c', 19, 23, 'circle',    'A', '01', '07', '02'],
        ['A07d', 20, 23, 'circle',    'A', '01', '07', '03'],
        ['A08a', 22, 24, 'circle',    'A', '01', '08', '01'],
        ['A08b', 23, 24, 'rectangle', 'A', '01', '08', '00'],
        ['A08c', 22, 23, 'circle',    'A', '01', '08', '02'],
        ['A08d', 23, 23, 'circle',    'A', '01', '08', '03'],
        ['A09a', 25, 24, 'circle',    'A', '01', '09', '01'],
        ['A09b', 26, 24, 'rectangle', 'A', '01', '09', '00'],
        ['A09c', 25, 23, 'circle',    'A', '01', '09', '02'],
        ['A09d', 26, 23, 'circle',    'A', '01', '09', '03'],
        ['A10a', 28, 24, 'circle',    'A', '01', '10', '01'],
        ['A10b', 29, 24, 'rectangle', 'A', '01', '10', '00'],
        ['A10c', 28, 23, 'circle',    'A', '01', '10', '02'],
        ['A10d', 29, 23, 'circle',    'A', '01', '10', '03'],
        ['A11a', 31, 24, 'circle',    'A', '01', '11', '01'],
        ['A11b', 32, 24, 'rectangle', 'A', '01', '11', '00'],
        ['A11c', 31, 23, 'circle',    'A', '01', '11', '02'],
        ['A11d', 32, 23, 'circle',    'A', '01', '11', '03'],
        ['A12a', 34, 24, 'circle',    'A', '01', '12', '01'],
        ['A12b', 35, 24, 'rectangle', 'A', '01', '12', '00'],
        ['A12c', 34, 23, 'circle',    'A', '01', '12', '02'],
        ['A12d', 35, 23, 'circle',    'A', '01', '12', '03'],

        ['B01a', 1, 21, 'circle',        'B', '02', '01', '01'],
        ['B01b', 2, 21, 'rectangle',     'B', '02', '01', '00'],
        ['B01c', 1, 20, 'circle',        'B', '02', '01', '02'],
        ['B01d', 2, 20, 'circle',        'B', '02', '01', '03'],
        ['B02a', 4, 21, 'circle',        'B', '02', '02', '01'],
        ['B02b', 5, 21, 'rectangle',     'B', '02', '02', '00'],
        ['B02c', 4, 20, 'circle',        'B', '02', '02', '02'],
        ['B02d', 5, 20, 'circle',        'B', '02', '02', '03'],
        ['B03a', 7, 21, 'circle',        'B', '02', '03', '01'],
        ['B03b', 8, 21, 'rectangle',     'B', '02', '03', '00'],
        ['B03c', 7, 20, 'circle',        'B', '02', '03', '02'],
        ['B03d', 8, 20, 'circle',        'B', '02', '03', '03'],
        ['B04a', 10, 21, 'circle',       'B', '02', '04', '01'],
        ['B04b', 11, 21, 'rectangle',    'B', '02', '04', '00'],
        ['B04c', 10, 20, 'circle',       'B', '02', '04', '02'],
        ['B04d', 11, 20, 'circle',       'B', '02', '04', '03'],
        ['B05a', 13, 21, 'circle',       'B', '02', '05', '01'],
        ['B05b', 14, 21, 'rectangle',    'B', '02', '05', '00'],
        ['B05c', 13, 20, 'circle',       'B', '02', '05', '02'],
        ['B05d', 14, 20, 'circle',       'B', '02', '05', '03'],
        ['B06a', 16, 21, 'circle',       'B', '02', '06', '01'],
        ['B06b', 17, 21, 'rectangle',    'B', '02', '06', '00'],
        ['B06c', 16, 20, 'circle',       'B', '02', '06', '02'],
        ['B06d', 17, 20, 'circle',       'B', '02', '06', '03'],
        ['B07a', 19, 21, 'circle',       'B', '02', '07', '01'],
        ['B07b', 20, 21, 'rectangle',    'B', '02', '07', '00'],
        ['B07c', 19, 20, 'circle',       'B', '02', '07', '02'],
        ['B07d', 20, 20, 'circle',       'B', '02', '07', '03'],
        ['B08a', 22, 21, 'circle',       'B', '02', '08', '01'],
        ['B08b', 23, 21, 'rectangle',    'B', '02', '08', '00'],
        ['B08c', 22, 20, 'circle',       'B', '02', '08', '02'],
        ['B08d', 23, 20, 'circle',       'B', '02', '08', '03'],
        ['B09a', 25, 21, 'circle',       'B', '02', '09', '01'],
        ['B09b', 26, 21, 'rectangle',    'B', '02', '09', '00'],
        ['B09c', 25, 20, 'circle',       'B', '02', '09', '02'],
        ['B09d', 26, 20, 'circle',       'B', '02', '09', '03'],
        ['B10a', 28, 21, 'circle',       'B', '02', '10', '01'],
        ['B10b', 29, 21, 'rectangle',    'B', '02', '10', '00'],
        ['B10c', 28, 20, 'circle',       'B', '02', '10', '02'],
        ['B10d', 29, 20, 'circle',       'B', '02', '10', '03'],
        ['B11a', 31, 21, 'circle',       'B', '02', '11', '01'],
        ['B11b', 32, 21, 'rectangle',    'B', '02', '11', '00'],
        ['B11c', 31, 20, 'circle',       'B', '02', '11', '02'],
        ['B11d', 32, 20, 'circle',       'B', '02', '11', '03'],
        ['B12a', 34, 21, 'circle',       'B', '02', '12', '01'],
        ['B12b', 35, 21, 'rectangle',    'B', '02', '12', '00'],
        ['B12c', 34, 20, 'circle',       'B', '02', '12', '02'],
        ['B12d', 35, 20, 'circle',       'B', '02', '12', '03'],

        ['C01a', 1, 18, 'circle',         'C', '03', '01', '01'],
        ['C01C', 2, 18, 'rectangle',      'C', '03', '01', '00'],
        ['C01c', 1, 17, 'circle',         'C', '03', '01', '02'],
        ['C01d', 2, 17, 'circle',         'C', '03', '01', '03'],
        ['C02a', 4, 18, 'circle',         'C', '03', '02', '01'],
        ['C02C', 5, 18, 'rectangle',      'C', '03', '02', '00'],
        ['C02c', 4, 17, 'circle',         'C', '03', '02', '02'],
        ['C02d', 5, 17, 'circle',         'C', '03', '02', '03'],
        ['C03a', 7, 18, 'circle',         'C', '03', '03', '01'],
        ['C03C', 8, 18, 'rectangle',      'C', '03', '03', '00'],
        ['C03c', 7, 17, 'circle',         'C', '03', '03', '02'],
        ['C03d', 8, 17, 'circle',         'C', '03', '03', '03'],
        ['C04a', 10, 18, 'circle',        'C', '03', '04', '01'],
        ['C04C', 11, 18, 'rectangle',     'C', '03', '04', '00'],
        ['C04c', 10, 17, 'circle',        'C', '03', '04', '02'],
        ['C04d', 11, 17, 'circle',        'C', '03', '04', '03'],
        ['C05a', 13, 18, 'circle',        'C', '03', '05', '01'],
        ['C05C', 14, 18, 'rectangle',     'C', '03', '05', '00'],
        ['C05c', 13, 17, 'circle',        'C', '03', '05', '02'],
        ['C05d', 14, 17, 'circle',        'C', '03', '05', '03'],
        ['C06a', 16, 18, 'circle',        'C', '03', '06', '01'],
        ['C06C', 17, 18, 'rectangle',     'C', '03', '06', '00'],
        ['C06c', 16, 17, 'circle',        'C', '03', '06', '02'],
        ['C06d', 17, 17, 'circle',        'C', '03', '06', '03'],
        ['C07a', 19, 18, 'circle',        'C', '03', '07', '01'],
        ['C07C', 20, 18, 'rectangle',     'C', '03', '07', '00'],
        ['C07c', 19, 17, 'circle',        'C', '03', '07', '02'],
        ['C07d', 20, 17, 'circle',        'C', '03', '07', '03'],
        ['C08a', 22, 18, 'circle',        'C', '03', '08', '01'],
        ['C08C', 23, 18, 'rectangle',     'C', '03', '08', '00'],
        ['C08c', 22, 17, 'circle',        'C', '03', '08', '02'],
        ['C08d', 23, 17, 'circle',        'C', '03', '08', '03'],
        ['C09a', 25, 18, 'circle',        'C', '03', '09', '01'],
        ['C09C', 26, 18, 'rectangle',     'C', '03', '09', '00'],
        ['C09c', 25, 17, 'circle',        'C', '03', '09', '02'],
        ['C09d', 26, 17, 'circle',        'C', '03', '09', '03'],
        ['C10a', 28, 18, 'circle',        'C', '03', '10', '01'],
        ['C10C', 29, 18, 'rectangle',     'C', '03', '10', '00'],
        ['C10c', 28, 17, 'circle',        'C', '03', '10', '02'],
        ['C10d', 29, 17, 'circle',        'C', '03', '10', '03'],
        ['C11a', 31, 18, 'circle',        'C', '03', '11', '01'],
        ['C11C', 32, 18, 'rectangle',     'C', '03', '11', '00'],
        ['C11c', 31, 17, 'circle',        'C', '03', '11', '02'],
        ['C11d', 32, 17, 'circle',        'C', '03', '11', '03'],
        ['C12a', 34, 18, 'circle',        'C', '03', '12', '01'],
        ['C12C', 35, 18, 'rectangle',     'C', '03', '12', '00'],
        ['C12c', 34, 17, 'circle',        'C', '03', '12', '02'],
        ['C12d', 35, 17, 'circle',        'C', '03', '12', '03'],

        ['D01a', 1, 15, 'circle',        'D', '04', '01', '01'],
        ['D01b', 2, 15, 'rectangle',     'D', '04', '01', '00'],
        ['D01c', 1, 14, 'circle',        'D', '04', '01', '02'],
        ['D01d', 2, 14, 'circle',        'D', '04', '01', '03'],
        ['D02a', 4, 15, 'circle',        'D', '04', '02', '01'],
        ['D02b', 5, 15, 'rectangle',     'D', '04', '02', '00'],
        ['D02c', 4, 14, 'circle',        'D', '04', '02', '02'],
        ['D02d', 5, 14, 'circle',        'D', '04', '02', '03'],
        ['D03a', 7, 15, 'circle',        'D', '04', '03', '01'],
        ['D03b', 8, 15, 'rectangle',     'D', '04', '03', '00'],
        ['D03c', 7, 14, 'circle',        'D', '04', '03', '02'],
        ['D03d', 8, 14, 'circle',        'D', '04', '03', '03'],
        ['D04a', 10, 15, 'circle',       'D', '04', '04', '01'],
        ['D04b', 11, 15, 'rectangle',    'D', '04', '04', '00'],
        ['D04c', 10, 14, 'circle',       'D', '04', '04', '02'],
        ['D04d', 11, 14, 'circle',       'D', '04', '04', '03'],
        ['D05a', 13, 15, 'circle',       'D', '04', '05', '01'],
        ['D05b', 14, 15, 'rectangle',    'D', '04', '05', '00'],
        ['D05c', 13, 14, 'circle',       'D', '04', '05', '02'],
        ['D05d', 14, 14, 'circle',       'D', '04', '05', '03'],
        ['D06a', 16, 15, 'circle',       'D', '04', '06', '01'],
        ['D06b', 17, 15, 'rectangle',    'D', '04', '06', '00'],
        ['D06c', 16, 14, 'circle',       'D', '04', '06', '02'],
        ['D06d', 17, 14, 'circle',       'D', '04', '06', '03'],
        ['D07a', 19, 15, 'circle',       'D', '04', '07', '01'],
        ['D07b', 20, 15, 'rectangle',    'D', '04', '07', '00'],
        ['D07c', 19, 14, 'circle',       'D', '04', '07', '02'],
        ['D07d', 20, 14, 'circle',       'D', '04', '07', '03'],
        ['D08a', 22, 15, 'circle',       'D', '04', '08', '01'],
        ['D08b', 23, 15, 'rectangle',    'D', '04', '08', '00'],
        ['D08c', 22, 14, 'circle',       'D', '04', '08', '02'],
        ['D08d', 23, 14, 'circle',       'D', '04', '08', '03'],
        ['D09a', 25, 15, 'circle',       'D', '04', '09', '01'],
        ['D09b', 26, 15, 'rectangle',    'D', '04', '09', '00'],
        ['D09c', 25, 14, 'circle',       'D', '04', '09', '02'],
        ['D09d', 26, 14, 'circle',       'D', '04', '09', '03'],
        ['D10a', 28, 15, 'circle',       'D', '04', '10', '01'],
        ['D10b', 29, 15, 'rectangle',    'D', '04', '10', '00'],
        ['D10c', 28, 14, 'circle',       'D', '04', '10', '02'],
        ['D10d', 29, 14, 'circle',       'D', '04', '10', '03'],
        ['D11a', 31, 15, 'circle',       'D', '04', '11', '01'],
        ['D11b', 32, 15, 'rectangle',    'D', '04', '11', '00'],
        ['D11c', 31, 14, 'circle',       'D', '04', '11', '02'],
        ['D11d', 32, 14, 'circle',       'D', '04', '11', '03'],
        ['D12a', 34, 15, 'circle',       'D', '04', '12', '01'],
        ['D12b', 35, 15, 'rectangle',    'D', '04', '12', '00'],
        ['D12c', 34, 14, 'circle',       'D', '04', '12', '02'],
        ['D12d', 35, 14, 'circle',       'D', '04', '12', '03'],

        ['E01a', 1, 12, 'circle',       'E', '05', '01', '01'], 
        ['E01E', 2, 12, 'rectangle',    'E', '05', '01', '00'], 
        ['E01c', 1, 11, 'circle',       'E', '05', '01', '02'], 
        ['E01d', 2, 11, 'circle',       'E', '05', '01', '03'],
        ['E02a', 4, 12, 'circle',       'E', '05', '02', '01'], 
        ['E02E', 5, 12, 'rectangle',    'E', '05', '02', '00'], 
        ['E02c', 4, 11, 'circle',       'E', '05', '02', '02'], 
        ['E02d', 5, 11, 'circle',       'E', '05', '02', '03'],
        ['E03a', 7, 12, 'circle',       'E', '05', '03', '01'], 
        ['E03E', 8, 12, 'rectangle',    'E', '05', '03', '00'], 
        ['E03c', 7, 11, 'circle',       'E', '05', '03', '02'], 
        ['E03d', 8, 11, 'circle',       'E', '05', '03', '03'],
        ['E04a', 10, 12, 'circle',      'E', '05', '04', '01'], 
        ['E04E', 11, 12, 'rectangle',   'E', '05', '04', '00'], 
        ['E04c', 10, 11, 'circle',      'E', '05', '04', '02'], 
        ['E04d', 11, 11, 'circle',      'E', '05', '04', '03'],
        ['E05a', 13, 12, 'circle',      'E', '05', '05', '01'], 
        ['E05E', 14, 12, 'rectangle',   'E', '05', '05', '00'], 
        ['E05c', 13, 11, 'circle',      'E', '05', '05', '02'], 
        ['E05d', 14, 11, 'circle',      'E', '05', '05', '03'],
        ['E06a', 16, 12, 'circle',      'E', '05', '06', '01'], 
        ['E06E', 17, 12, 'rectangle',   'E', '05', '06', '00'], 
        ['E06c', 16, 11, 'circle',      'E', '05', '06', '02'], 
        ['E06d', 17, 11, 'circle',      'E', '05', '06', '03'],
        ['E07a', 19, 12, 'circle',      'E', '05', '07', '01'], 
        ['E07E', 20, 12, 'rectangle',   'E', '05', '07', '00'], 
        ['E07c', 19, 11, 'circle',      'E', '05', '07', '02'], 
        ['E07d', 20, 11, 'circle',      'E', '05', '07', '03'],
        ['E08a', 22, 12, 'circle',      'E', '05', '08', '01'], 
        ['E08E', 23, 12, 'rectangle',   'E', '05', '08', '00'], 
        ['E08c', 22, 11, 'circle',      'E', '05', '08', '02'], 
        ['E08d', 23, 11, 'circle',      'E', '05', '08', '03'],
        ['E09a', 25, 12, 'circle',      'E', '05', '09', '01'], 
        ['E09E', 26, 12, 'rectangle',   'E', '05', '09', '00'], 
        ['E09c', 25, 11, 'circle',      'E', '05', '09', '02'], 
        ['E09d', 26, 11, 'circle',      'E', '05', '09', '03'],
        ['E10a', 28, 12, 'circle',      'E', '05', '10', '01'], 
        ['E10E', 29, 12, 'rectangle',   'E', '05', '10', '00'], 
        ['E10c', 28, 11, 'circle',      'E', '05', '10', '02'], 
        ['E10d', 29, 11, 'circle',      'E', '05', '10', '03'],
        ['E11a', 31, 12, 'circle',      'E', '05', '11', '01'], 
        ['E11E', 32, 12, 'rectangle',   'E', '05', '11', '00'], 
        ['E11c', 31, 11, 'circle',      'E', '05', '11', '02'], 
        ['E11d', 32, 11, 'circle',      'E', '05', '11', '03'],
        ['E12a', 34, 12, 'circle',      'E', '05', '12', '01'], 
        ['E12E', 35, 12, 'rectangle',   'E', '05', '12', '00'], 
        ['E12c', 34, 11, 'circle',      'E', '05', '12', '02'], 
        ['E12d', 35, 11, 'circle',      'E', '05', '12', '03'],

        ['F01a', 1, 9, 'circle',       'F', '06', '01', '01'],
        ['F01F', 2, 9, 'rectangle',    'F', '06', '01', '00'],
        ['F01c', 1, 8, 'circle',       'F', '06', '01', '02'],
        ['F01d', 2, 8, 'circle',       'F', '06', '01', '03'],
        ['F02a', 4, 9, 'circle',       'F', '06', '02', '01'],
        ['F02F', 5, 9, 'rectangle',    'F', '06', '02', '00'],
        ['F02c', 4, 8, 'circle',       'F', '06', '02', '02'],
        ['F02d', 5, 8, 'circle',       'F', '06', '02', '03'],
        ['F03a', 7, 9, 'circle',       'F', '06', '03', '01'],
        ['F03F', 8, 9, 'rectangle',    'F', '06', '03', '00'],
        ['F03c', 7, 8, 'circle',       'F', '06', '03', '02'],
        ['F03d', 8, 8, 'circle',       'F', '06', '03', '03'],
        ['F04a', 10, 9, 'circle',      'F', '06', '04', '01'],
        ['F04F', 11, 9, 'rectangle',   'F', '06', '04', '00'],
        ['F04c', 10, 8, 'circle',      'F', '06', '04', '02'],
        ['F04d', 11, 8, 'circle',      'F', '06', '04', '03'],
        ['F05a', 13, 9, 'circle',      'F', '06', '05', '01'],
        ['F05F', 14, 9, 'rectangle',   'F', '06', '05', '00'],
        ['F05c', 13, 8, 'circle',      'F', '06', '05', '02'],
        ['F05d', 14, 8, 'circle',      'F', '06', '05', '03'],
        ['F06a', 16, 9, 'circle',      'F', '06', '06', '01'],
        ['F06F', 17, 9, 'rectangle',   'F', '06', '06', '00'],
        ['F06c', 16, 8, 'circle',      'F', '06', '06', '02'],
        ['F06d', 17, 8, 'circle',      'F', '06', '06', '03'],
        ['F07a', 19, 9, 'circle',      'F', '06', '07', '01'],
        ['F07F', 20, 9, 'rectangle',   'F', '06', '07', '00'],
        ['F07c', 19, 8, 'circle',      'F', '06', '07', '02'],
        ['F07d', 20, 8, 'circle',      'F', '06', '07', '03'],
        ['F08a', 22, 9, 'circle',      'F', '06', '08', '01'],
        ['F08F', 23, 9, 'rectangle',   'F', '06', '08', '00'],
        ['F08c', 22, 8, 'circle',      'F', '06', '08', '02'],
        ['F08d', 23, 8, 'circle',      'F', '06', '08', '03'],
        ['F09a', 25, 9, 'circle',      'F', '06', '09', '01'],
        ['F09F', 26, 9, 'rectangle',   'F', '06', '09', '00'],
        ['F09c', 25, 8, 'circle',      'F', '06', '09', '02'],
        ['F09d', 26, 8, 'circle',      'F', '06', '09', '03'],
        ['F10a', 28, 9, 'circle',      'F', '06', '10', '01'],
        ['F10F', 29, 9, 'rectangle',   'F', '06', '10', '00'],
        ['F10c', 28, 8, 'circle',      'F', '06', '10', '02'],
        ['F10d', 29, 8, 'circle',      'F', '06', '10', '03'],
        ['F11a', 31, 9, 'circle',      'F', '06', '11', '01'],
        ['F11F', 32, 9, 'rectangle',   'F', '06', '11', '00'],
        ['F11c', 31, 8, 'circle',      'F', '06', '11', '02'],
        ['F11d', 32, 8, 'circle',      'F', '06', '11', '03'],
        ['F12a', 34, 9, 'circle',      'F', '06', '12', '01'],
        ['F12F', 35, 9, 'rectangle',   'F', '06', '12', '00'],
        ['F12c', 34, 8, 'circle',      'F', '06', '12', '02'],
        ['F12d', 35, 8, 'circle',      'F', '06', '12', '03'],

        ['G01a', 1, 6, 'circle',       'G', '07', '01', '01'],
        ['G01G', 2, 6, 'rectangle',    'G', '07', '01', '00'],
        ['G01c', 1, 5, 'circle',       'G', '07', '01', '02'],
        ['G01d', 2, 5, 'circle',       'G', '07', '01', '03'],
        ['G02a', 4, 6, 'circle',       'G', '07', '02', '01'],
        ['G02G', 5, 6, 'rectangle',    'G', '07', '02', '00'],
        ['G02c', 4, 5, 'circle',       'G', '07', '02', '02'],
        ['G02d', 5, 5, 'circle',       'G', '07', '02', '03'],
        ['G03a', 7, 6, 'circle',       'G', '07', '03', '01'],
        ['G03G', 8, 6, 'rectangle',    'G', '07', '03', '00'],
        ['G03c', 7, 5, 'circle',       'G', '07', '03', '02'],
        ['G03d', 8, 5, 'circle',       'G', '07', '03', '03'],
        ['G04a', 10, 6, 'circle',      'G', '07', '04', '01'],
        ['G04G', 11, 6, 'rectangle',   'G', '07', '04', '00'],
        ['G04c', 10, 5, 'circle',      'G', '07', '04', '02'],
        ['G04d', 11, 5, 'circle',      'G', '07', '04', '03'],
        ['G05a', 13, 6, 'circle',      'G', '07', '05', '01'],
        ['G05G', 14, 6, 'rectangle',   'G', '07', '05', '00'],
        ['G05c', 13, 5, 'circle',      'G', '07', '05', '02'],
        ['G05d', 14, 5, 'circle',      'G', '07', '05', '03'],
        ['G06a', 16, 6, 'circle',      'G', '07', '06', '01'],
        ['G06G', 17, 6, 'rectangle',   'G', '07', '06', '00'],
        ['G06c', 16, 5, 'circle',      'G', '07', '06', '02'],
        ['G06d', 17, 5, 'circle',      'G', '07', '06', '03'],
        ['G07a', 19, 6, 'circle',      'G', '07', '07', '01'],
        ['G07G', 20, 6, 'rectangle',   'G', '07', '07', '00'],
        ['G07c', 19, 5, 'circle',      'G', '07', '07', '02'],
        ['G07d', 20, 5, 'circle',      'G', '07', '07', '03'],
        ['G08a', 22, 6, 'circle',      'G', '07', '08', '01'],
        ['G08G', 23, 6, 'rectangle',   'G', '07', '08', '00'],
        ['G08c', 22, 5, 'circle',      'G', '07', '08', '02'],
        ['G08d', 23, 5, 'circle',      'G', '07', '08', '03'],
        ['G09a', 25, 6, 'circle',      'G', '07', '09', '01'],
        ['G09G', 26, 6, 'rectangle',   'G', '07', '09', '00'],
        ['G09c', 25, 5, 'circle',      'G', '07', '09', '02'],
        ['G09d', 26, 5, 'circle',      'G', '07', '09', '03'],
        ['G10a', 28, 6, 'circle',      'G', '07', '10', '01'],
        ['G10G', 29, 6, 'rectangle',   'G', '07', '10', '00'],
        ['G10c', 28, 5, 'circle',      'G', '07', '10', '02'],
        ['G10d', 29, 5, 'circle',      'G', '07', '10', '03'],
        ['G11a', 31, 6, 'circle',      'G', '07', '11', '01'],
        ['G11G', 32, 6, 'rectangle',   'G', '07', '11', '00'],
        ['G11c', 31, 5, 'circle',      'G', '07', '11', '02'],
        ['G11d', 32, 5, 'circle',      'G', '07', '11', '03'],
        ['G12a', 34, 6, 'circle',      'G', '07', '12', '01'],
        ['G12G', 35, 6, 'rectangle',   'G', '07', '12', '00'],
        ['G12c', 34, 5, 'circle',      'G', '07', '12', '02'],
        ['G12d', 35, 5, 'circle',      'G', '07', '12', '03'],

        ['H01a', 1, 3, 'circle',       'H', '08', '01', '01'],
        ['H01H', 2, 3, 'rectangle',    'H', '08', '01', '00'],
        ['H01c', 1, 2, 'circle',       'H', '08', '01', '02'],
        ['H01d', 2, 2, 'circle',       'H', '08', '01', '03'],
        ['H02a', 4, 3, 'circle',       'H', '08', '02', '01'],
        ['H02H', 5, 3, 'rectangle',    'H', '08', '02', '00'],
        ['H02c', 4, 2, 'circle',       'H', '08', '02', '02'],
        ['H02d', 5, 2, 'circle',       'H', '08', '02', '03'],
        ['H03a', 7, 3, 'circle',       'H', '08', '03', '01'],
        ['H03H', 8, 3, 'rectangle',    'H', '08', '03', '00'],
        ['H03c', 7, 2, 'circle',       'H', '08', '03', '02'],
        ['H03d', 8, 2, 'circle',       'H', '08', '03', '03'],
        ['H04a', 10, 3, 'circle',      'H', '08', '04', '01'],
        ['H04H', 11, 3, 'rectangle',   'H', '08', '04', '00'],
        ['H04c', 10, 2, 'circle',      'H', '08', '04', '02'],
        ['H04d', 11, 2, 'circle',      'H', '08', '04', '03'],
        ['H05a', 13, 3, 'circle',      'H', '08', '05', '01'],
        ['H05H', 14, 3, 'rectangle',   'H', '08', '05', '00'],
        ['H05c', 13, 2, 'circle',      'H', '08', '05', '02'],
        ['H05d', 14, 2, 'circle',      'H', '08', '05', '03'],
        ['H06a', 16, 3, 'circle',      'H', '08', '06', '01'],
        ['H06H', 17, 3, 'rectangle',   'H', '08', '06', '00'],
        ['H06c', 16, 2, 'circle',      'H', '08', '06', '02'],
        ['H06d', 17, 2, 'circle',      'H', '08', '06', '03'],
        ['H07a', 19, 3, 'circle',      'H', '08', '07', '01'],
        ['H07H', 20, 3, 'rectangle',   'H', '08', '07', '00'],
        ['H07c', 19, 2, 'circle',      'H', '08', '07', '02'],
        ['H07d', 20, 2, 'circle',      'H', '08', '07', '03'],
        ['H08a', 22, 3, 'circle',      'H', '08', '08', '01'],
        ['H08H', 23, 3, 'rectangle',   'H', '08', '08', '00'],
        ['H08c', 22, 2, 'circle',      'H', '08', '08', '02'],
        ['H08d', 23, 2, 'circle',      'H', '08', '08', '03'],
        ['H09a', 25, 3, 'circle',      'H', '08', '09', '01'],
        ['H09H', 26, 3, 'rectangle',   'H', '08', '09', '00'],
        ['H09c', 25, 2, 'circle',      'H', '08', '09', '02'],
        ['H09d', 26, 2, 'circle',      'H', '08', '09', '03'],
        ['H10a', 28, 3, 'circle',      'H', '08', '10', '01'],
        ['H10H', 29, 3, 'rectangle',   'H', '08', '10', '00'],
        ['H10c', 28, 2, 'circle',      'H', '08', '10', '02'],
        ['H10d', 29, 2, 'circle',      'H', '08', '10', '03'],
        ['H11a', 31, 3, 'circle',      'H', '08', '11', '01'],
        ['H11H', 32, 3, 'rectangle',   'H', '08', '11', '00'],
        ['H11c', 31, 2, 'circle',      'H', '08', '11', '02'],
        ['H11d', 32, 2, 'circle',      'H', '08', '11', '03'],
        ['H12a', 34, 3, 'circle',      'H', '08', '12', '01'],
        ['H12H', 35, 3, 'rectangle',   'H', '08', '12', '00'],
        ['H12c', 34, 2, 'circle',      'H', '08', '12', '02'],
        ['H12d', 35, 2, 'circle',      'H', '08', '12', '03']

    ]
    return coordinates

def get_coordinates_from_filename(crystal_image, plate_layout):
    x = None
    y = None
    column, row, subwell = get_row_column_subwell_from_filename(crystal_image)
    if crystal_image:
        for c in plate_layout:
            if c[6] == column and c[5] == row and c[7] == subwell:
                x = c[1]
                y = c[2]
                break
    return x, y

def get_row_column_subwell_from_filename(crystal_image):
    column = None
    row = None
    subwell = None
    if crystal_image:
        fn = os.path.basename(crystal_image)
        column = fn.split('_')[10]
        row = fn.split('_')[11]
        subwell = fn.split('_')[12]
    return column, row, subwell

def get_row_letter_column_subwell_from_filename(crystal_image):
    column = None
    subwell = None
    row_letter = None
    if crystal_image:
        fn = os.path.basename(crystal_image)
        column = fn.split('_')[10]
        row = fn.split('_')[11]
        row_letter = get_row_letter_from_row_number(row, swiss_ci_3_drop_layout())
        subwell = fn.split('_')[12]
    return column, row_letter, subwell

def get_row_letter_column_subwell_well_from_filename(crystal_image):
    column = None
    subwell = None
    row_letter = None
    well = None
    if crystal_image:
        fn = os.path.basename(crystal_image)
        column = fn.split('_')[10]
        row = fn.split('_')[11]
        row_letter = get_row_letter_from_row_number(row, swiss_ci_3_drop_layout())
        well = row_letter + str(int(column))
        subwell = fn.split('_')[12]
    return column, row_letter, subwell, well

def get_row_letter_from_row_number(row_number, plate_layout):
    row_letter = None
    for r in plate_layout:
        if r[5] == row_number:
            row_letter = r[4]
            break
    return row_letter

def get_list_of_dict_from_marked_crystal_list(marked_crystal_list, barcode):
    l = []
    for item in marked_crystal_list:
        row_letter = item[2]
        column = item[3]
        subwell = item[4]
        d = {}
        d['crystal_plate_barcode'] = barcode
        d['crystal_plate_row'] = row_letter
        d['crystal_plate_column'] = column
        d['crystal_plate_subwell'] = subwell
        d['crystal_plate_well'] = d['crystal_plate_row'] + d['crystal_plate_column']
#        d['marked_crystal_code'] = d['crystal_plate_barcode'] + '-' + d['crystal_plate_well'] + d['crystal_plate_subwell']
        d['marked_crystal_code'] = "{0!s}-{1!s}-{2!s}-{3!s}".format(barcode, row_letter, int(column), int(subwell))
        l.append(d)
    return l

def get_shifter_csv_header():
    header = [
        'PlateType',
        'PlateID',
        'LocationShifter',
        'PlateColumn',
        'PlateRow',
        'PositionSubWell',
        'Comment',
        'CrystalID',
        'TimeArrival',
        'TimeDeparture',
        'PickDuration',
        'DestinationName',
        'DestinationLocation',
        'Barcode',
        'ExternalComment'
        ]
    return header

def crystal_plate_header():
    header = [
        'plate_type_name',
        'crystal_plate_barcode',
        'crystal_plate_row',
        'crystal_plate_column',
        'crystal_plate_subwell',
        'crystal_plate_well',
        'status',
        'soak_plate_name',
        'soak_plate_well'
    ]
    return header

def get_step_for_progress_bar(steps):
    start = 0.0
    step = float(100/int(steps))
    return start, step

def backup_file(logger, folder, file_name):
    if os.path.isfile(os.path.join(folder, file_name)):
        logger.warning('file exists ' + os.path.join(folder, file_name))
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logger.info('backing up exisiting file as ' + file_name + now)
        copyfile(os.path.join(folder, file_name),
                 os.path.join(folder, 'backup', file_name + '.' + now))

def read_line_from_shifter_csv(logger, line):
    if line.startswith(';'):
        s = {}
    elif line.startswith('PlateType'):
        s = {}
    elif line.startswith('";'):
        s = {}
    elif line.startswith('"'):
        s = {}
    elif line.startswith("Column1"):
        s = {}
    else:
        try:
#            s = {
#                'PlateType':            re.split(r'[,;]+', line)[0],
#                'PlateID':              re.split(r'[,;]+', line)[1],
#                'LocationShifter':      re.split(r'[,;]+', line)[2],
#                'PlateRow':             re.split(r'[,;]+', line)[3],
#                'PlateColumn':          re.split(r'[,;]+', line)[4],
#                'PositionSubWell':      re.split(r'[,;]+', line)[5],
#                'Comment':              re.split(r'[,;]+', line)[6],
#                'CrystalID':            re.split(r'[,;]+', line)[7],
#                'TimeArrival':          re.split(r'[,;]+', line)[8],
#                'TimeDeparture':        re.split(r'[,;]+', line)[9],
#                'PickDuration':         re.split(r'[,;]+', line)[10],
#                'DestinationName':      re.split(r'[,;]+', line)[11],
#                'DestinationLocation':  re.split(r'[,;]+', line)[12],
#                'Barcode':              re.split(r'[,;]+', line)[13],
#                'ExternalComment':      re.split(r'[,;]+', line)[14]
#            }
            s = {
                'PlateType':            line.split(",")[0],
                'PlateID':              line.split(",")[1],
                'LocationShifter':      line.split(",")[2],
                'PlateRow':             line.split(",")[3],
                'PlateColumn':          line.split(",")[4],
                'PositionSubWell':      line.split(",")[5],
                'Comment':              line.split(",")[6],
                'CrystalID':            line.split(",")[7],
                'TimeArrival':          line.split(",")[8],
                'TimeDeparture':        line.split(",")[9],
                'PickDuration':         line.split(",")[10],
                'DestinationName':      line.split(",")[11],
                'DestinationLocation':  line.split(",")[12],
                'Barcode':              line.split(",")[13],
                'ExternalComment':      line.split(",")[14]
            }
        except IndexError:
            logger.warning('seems there are marked but not mounted crystals in file (check info line below):')
#            logger.info(str(re.split(r'[,;]+', line)))
            logger.info(str(line.split(",")))
            s = {}
    return s

def read_line_from_shifter_csv_as_mounted_crystal_dict(logger, line):
    s = read_line_from_shifter_csv(logger, line)
    mount_dict = {}
    soak_dict = {}
    if s:
        well = s['PlateRow'] + (2 - len(s['PlateColumn'])) * '0' + s['PlateColumn']
        subwell = subwell_letter_to_numeric(s['PositionSubWell'])
#        soak_dict['marked_crystal_code'] = s['PlateID'] + '-' + well + '-' + subwell
        soak_dict['marked_crystal_code'] = "{0!s}-{1!s}-{2!s}-{3!s}".format(s['PlateID'], s['PlateRow'],
                                                                            s['PlateColumn'], int(subwell))
        soak_dict['status'] = s['Comment'].split(':')[0]
        soak_dict['compound_appearance'] = s['Comment'].split(':')[1]
        soak_dict['crystal_appearance'] = s['Comment'].split(':')[2]
        if not 'fail' in s['Comment'].lower():
            mount_dict['puck_name'] = s['DestinationName']
            mount_dict['puck_position'] = s['DestinationLocation']
            # time format: "15/03/2023 09:11:27"
            mount_dict['mount_datetime'] = datetime.strptime(s['TimeDeparture'], '%d/%m/%Y %H:%M:%S')
            mount_dict['marked_crystal_code'] = soak_dict['marked_crystal_code']
            mount_dict['compound_appearance'] = soak_dict['compound_appearance']
            mount_dict['crystal_appearance'] = soak_dict['crystal_appearance']
    return mount_dict, soak_dict

def numeric_subwell_to_letter(num_subwell):
    subwell = num_subwell
    if num_subwell == '01':
        subwell = 'a'
    elif num_subwell == '02':
        subwell = 'c'
    elif num_subwell == '03':
        subwell = 'd'
    return subwell

def subwell_letter_to_numeric(letter_subwell):
    subwell = letter_subwell
    if letter_subwell == 'a':
        subwell = '01'
    elif letter_subwell == 'c':
        subwell = '02'
    elif letter_subwell == 'd':
        subwell = '03'
    return subwell