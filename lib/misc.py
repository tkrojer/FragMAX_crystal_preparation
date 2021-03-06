import re

def swiss_ci_layout():

    coordinates = [
        ['A01a', 1, 24, 'circle'], ['A01b', 2, 24, 'rectangle'], ['A01c', 1, 23, 'circle'], ['A01d', 2, 23, 'circle'],
        ['A02a', 4, 24, 'circle'], ['A02b', 5, 24, 'rectangle'], ['A02c', 4, 23, 'circle'], ['A02d', 5, 23, 'circle'],
        ['A03a', 7, 24, 'circle'], ['A03b', 8, 24, 'rectangle'], ['A03c', 7, 23, 'circle'], ['A03d', 8, 23, 'circle'],
        ['A04a', 10, 24, 'circle'], ['A04b', 11, 24, 'rectangle'], ['A04c', 10, 23, 'circle'], ['A04d', 11, 23, 'circle'],
        ['A05a', 13, 24, 'circle'], ['A05b', 14, 24, 'rectangle'], ['A05c', 13, 23, 'circle'], ['A05d', 14, 23, 'circle'],
        ['A06a', 16, 24, 'circle'], ['A06b', 17, 24, 'rectangle'], ['A06c', 16, 23, 'circle'], ['A06d', 17, 23, 'circle'],
        ['A07a', 19, 24, 'circle'], ['A07b', 20, 24, 'rectangle'], ['A07c', 19, 23, 'circle'], ['A07d', 20, 23, 'circle'],
        ['A08a', 22, 24, 'circle'], ['A08b', 23, 24, 'rectangle'], ['A08c', 22, 23, 'circle'], ['A08d', 23, 23, 'circle'],
        ['A09a', 25, 24, 'circle'], ['A09b', 26, 24, 'rectangle'], ['A09c', 25, 23, 'circle'], ['A09d', 26, 23, 'circle'],
        ['A10a', 28, 24, 'circle'], ['A10b', 29, 24, 'rectangle'], ['A10c', 28, 23, 'circle'], ['A10d', 29, 23, 'circle'],
        ['A11a', 31, 24, 'circle'], ['A11b', 32, 24, 'rectangle'], ['A11c', 31, 23, 'circle'], ['A11d', 32, 23, 'circle'],
    ['A12a', 34, 24, 'circle'], ['A12b', 35, 24, 'rectangle'], ['A12c', 34, 23, 'circle'], ['A12d', 35, 23, 'circle'],

    ['B01a', 1, 21, 'circle'], ['B01b', 2, 21, 'rectangle'], ['B01c', 1, 20, 'circle'], ['B01d', 2, 20, 'circle'],
    ['B02a', 4, 21, 'circle'], ['B02b', 5, 21, 'rectangle'], ['B02c', 4, 20, 'circle'], ['B02d', 5, 20, 'circle'],
    ['B03a', 7, 21, 'circle'], ['B03b', 8, 21, 'rectangle'], ['B03c', 7, 20, 'circle'], ['B03d', 8, 20, 'circle'],
    ['B04a', 10, 21, 'circle'], ['B04b', 11, 21, 'rectangle'], ['B04c', 10, 20, 'circle'], ['B04d', 11, 20, 'circle'],
    ['B05a', 13, 21, 'circle'], ['B05b', 14, 21, 'rectangle'], ['B05c', 13, 20, 'circle'], ['B05d', 14, 20, 'circle'],
    ['B06a', 16, 21, 'circle'], ['B06b', 17, 21, 'rectangle'], ['B06c', 16, 20, 'circle'], ['B06d', 17, 20, 'circle'],
    ['B07a', 19, 21, 'circle'], ['B07b', 20, 21, 'rectangle'], ['B07c', 19, 20, 'circle'], ['B07d', 20, 20, 'circle'],
    ['B08a', 22, 21, 'circle'], ['B08b', 23, 21, 'rectangle'], ['B08c', 22, 20, 'circle'], ['B08d', 23, 20, 'circle'],
    ['B09a', 25, 21, 'circle'], ['B09b', 26, 21, 'rectangle'], ['B09c', 25, 20, 'circle'], ['B09d', 26, 20, 'circle'],
    ['B10a', 28, 21, 'circle'], ['B10b', 29, 21, 'rectangle'], ['B10c', 28, 20, 'circle'], ['B10d', 29, 20, 'circle'],
    ['B11a', 31, 21, 'circle'], ['B11b', 32, 21, 'rectangle'], ['B11c', 31, 20, 'circle'], ['B11d', 32, 20, 'circle'],
    ['B12a', 34, 21, 'circle'], ['B12b', 35, 21, 'rectangle'], ['B12c', 34, 20, 'circle'], ['B12d', 35, 20, 'circle'],

    ['C01a', 1, 18, 'circle'], ['C01C', 2, 18, 'rectangle'], ['C01c', 1, 17, 'circle'], ['C01d', 2, 17, 'circle'],
    ['C02a', 4, 18, 'circle'], ['C02C', 5, 18, 'rectangle'], ['C02c', 4, 17, 'circle'], ['C02d', 5, 17, 'circle'],
    ['C03a', 7, 18, 'circle'], ['C03C', 8, 18, 'rectangle'], ['C03c', 7, 17, 'circle'], ['C03d', 8, 17, 'circle'],
    ['C04a', 10, 18, 'circle'], ['C04C', 11, 18, 'rectangle'], ['C04c', 10, 17, 'circle'], ['C04d', 11, 17, 'circle'],
    ['C05a', 13, 18, 'circle'], ['C05C', 14, 18, 'rectangle'], ['C05c', 13, 17, 'circle'], ['C05d', 14, 17, 'circle'],
    ['C06a', 16, 18, 'circle'], ['C06C', 17, 18, 'rectangle'], ['C06c', 16, 17, 'circle'], ['C06d', 17, 17, 'circle'],
    ['C07a', 19, 18, 'circle'], ['C07C', 20, 18, 'rectangle'], ['C07c', 19, 17, 'circle'], ['C07d', 20, 17, 'circle'],
    ['C08a', 22, 18, 'circle'], ['C08C', 23, 18, 'rectangle'], ['C08c', 22, 17, 'circle'], ['C08d', 23, 17, 'circle'],
    ['C09a', 25, 18, 'circle'], ['C09C', 26, 18, 'rectangle'], ['C09c', 25, 17, 'circle'], ['C09d', 26, 17, 'circle'],
    ['C10a', 28, 18, 'circle'], ['C10C', 29, 18, 'rectangle'], ['C10c', 28, 17, 'circle'], ['C10d', 29, 17, 'circle'],
    ['C11a', 31, 18, 'circle'], ['C11C', 32, 18, 'rectangle'], ['C11c', 31, 17, 'circle'], ['C11d', 32, 17, 'circle'],
    ['C12a', 34, 18, 'circle'], ['C12C', 35, 18, 'rectangle'], ['C12c', 34, 17, 'circle'], ['C12d', 35, 17, 'circle'],

    ['D01a', 1, 15, 'circle'], ['D01D', 2, 15, 'rectangle'], ['D01c', 1, 14, 'circle'], ['D01d', 2, 14, 'circle'],
    ['D02a', 4, 15, 'circle'], ['D02D', 5, 15, 'rectangle'], ['D02c', 4, 14, 'circle'], ['D02d', 5, 14, 'circle'],
    ['D03a', 7, 15, 'circle'], ['D03D', 8, 15, 'rectangle'], ['D03c', 7, 14, 'circle'], ['D03d', 8, 14, 'circle'],
    ['D04a', 10, 15, 'circle'], ['D04D', 11, 15, 'rectangle'], ['D04c', 10, 14, 'circle'], ['D04d', 11, 14, 'circle'],
    ['D05a', 13, 15, 'circle'], ['D05D', 14, 15, 'rectangle'], ['D05c', 13, 14, 'circle'], ['D05d', 14, 14, 'circle'],
    ['D06a', 16, 15, 'circle'], ['D06D', 17, 15, 'rectangle'], ['D06c', 16, 14, 'circle'], ['D06d', 17, 14, 'circle'],
    ['D07a', 19, 15, 'circle'], ['D07D', 20, 15, 'rectangle'], ['D07c', 19, 14, 'circle'], ['D07d', 20, 14, 'circle'],
    ['D08a', 22, 15, 'circle'], ['D08D', 23, 15, 'rectangle'], ['D08c', 22, 14, 'circle'], ['D08d', 23, 14, 'circle'],
    ['D09a', 25, 15, 'circle'], ['D09D', 26, 15, 'rectangle'], ['D09c', 25, 14, 'circle'], ['D09d', 26, 14, 'circle'],
    ['D10a', 28, 15, 'circle'], ['D10D', 29, 15, 'rectangle'], ['D10c', 28, 14, 'circle'], ['D10d', 29, 14, 'circle'],
    ['D11a', 31, 15, 'circle'], ['D11D', 32, 15, 'rectangle'], ['D11c', 31, 14, 'circle'], ['D11d', 32, 14, 'circle'],
    ['D12a', 34, 15, 'circle'], ['D12D', 35, 15, 'rectangle'], ['D12c', 34, 14, 'circle'], ['D12d', 35, 14, 'circle'],

    ['E01a', 1, 12, 'circle'], ['E01E', 2, 12, 'rectangle'], ['E01c', 1, 11, 'circle'], ['E01d', 2, 11, 'circle'],
    ['E02a', 4, 12, 'circle'], ['E02E', 5, 12, 'rectangle'], ['E02c', 4, 11, 'circle'], ['E02d', 5, 11, 'circle'],
    ['E03a', 7, 12, 'circle'], ['E03E', 8, 12, 'rectangle'], ['E03c', 7, 11, 'circle'], ['E03d', 8, 11, 'circle'],
    ['E04a', 10, 12, 'circle'], ['E04E', 11, 12, 'rectangle'], ['E04c', 10, 11, 'circle'], ['E04d', 11, 11, 'circle'],
    ['E05a', 13, 12, 'circle'], ['E05E', 14, 12, 'rectangle'], ['E05c', 13, 11, 'circle'], ['E05d', 14, 11, 'circle'],
    ['E06a', 16, 12, 'circle'], ['E06E', 17, 12, 'rectangle'], ['E06c', 16, 11, 'circle'], ['E06d', 17, 11, 'circle'],
    ['E07a', 19, 12, 'circle'], ['E07E', 20, 12, 'rectangle'], ['E07c', 19, 11, 'circle'], ['E07d', 20, 11, 'circle'],
    ['E08a', 22, 12, 'circle'], ['E08E', 23, 12, 'rectangle'], ['E08c', 22, 11, 'circle'], ['E08d', 23, 11, 'circle'],
    ['E09a', 25, 12, 'circle'], ['E09E', 26, 12, 'rectangle'], ['E09c', 25, 11, 'circle'], ['E09d', 26, 11, 'circle'],
    ['E10a', 28, 12, 'circle'], ['E10E', 29, 12, 'rectangle'], ['E10c', 28, 11, 'circle'], ['E10d', 29, 11, 'circle'],
    ['E11a', 31, 12, 'circle'], ['E11E', 32, 12, 'rectangle'], ['E11c', 31, 11, 'circle'], ['E11d', 32, 11, 'circle'],
    ['E12a', 34, 12, 'circle'], ['E12E', 35, 12, 'rectangle'], ['E12c', 34, 11, 'circle'], ['E12d', 35, 11, 'circle'],

    ['F01a', 1, 9, 'circle'], ['F01F', 2, 9, 'rectangle'], ['F01c', 1, 8, 'circle'], ['F01d', 2, 8, 'circle'],
    ['F02a', 4, 9, 'circle'], ['F02F', 5, 9, 'rectangle'], ['F02c', 4, 8, 'circle'], ['F02d', 5, 8, 'circle'],
    ['F03a', 7, 9, 'circle'], ['F03F', 8, 9, 'rectangle'], ['F03c', 7, 8, 'circle'], ['F03d', 8, 8, 'circle'],
    ['F04a', 10, 9, 'circle'], ['F04F', 11, 9, 'rectangle'], ['F04c', 10, 8, 'circle'], ['F04d', 11, 8, 'circle'],
    ['F05a', 13, 9, 'circle'], ['F05F', 14, 9, 'rectangle'], ['F05c', 13, 8, 'circle'], ['F05d', 14, 8, 'circle'],
    ['F06a', 16, 9, 'circle'], ['F06F', 17, 9, 'rectangle'], ['F06c', 16, 8, 'circle'], ['F06d', 17, 8, 'circle'],
    ['F07a', 19, 9, 'circle'], ['F07F', 20, 9, 'rectangle'], ['F07c', 19, 8, 'circle'], ['F07d', 20, 8, 'circle'],
    ['F08a', 22, 9, 'circle'], ['F08F', 23, 9, 'rectangle'], ['F08c', 22, 8, 'circle'], ['F08d', 23, 8, 'circle'],
    ['F09a', 25, 9, 'circle'], ['F09F', 26, 9, 'rectangle'], ['F09c', 25, 8, 'circle'], ['F09d', 26, 8, 'circle'],
    ['F10a', 28, 9, 'circle'], ['F10F', 29, 9, 'rectangle'], ['F10c', 28, 8, 'circle'], ['F10d', 29, 8, 'circle'],
    ['F11a', 31, 9, 'circle'], ['F11F', 32, 9, 'rectangle'], ['F11c', 31, 8, 'circle'], ['F11d', 32, 8, 'circle'],
    ['F12a', 34, 9, 'circle'], ['F12F', 35, 9, 'rectangle'], ['F12c', 34, 8, 'circle'], ['F12d', 35, 8, 'circle'],

    ['G01a', 1, 6, 'circle'], ['G01G', 2, 6, 'rectangle'], ['G01c', 1, 5, 'circle'], ['G01d', 2, 5, 'circle'],
    ['G02a', 4, 6, 'circle'], ['G02G', 5, 6, 'rectangle'], ['G02c', 4, 5, 'circle'], ['G02d', 5, 5, 'circle'],
    ['G03a', 7, 6, 'circle'], ['G03G', 8, 6, 'rectangle'], ['G03c', 7, 5, 'circle'], ['G03d', 8, 5, 'circle'],
    ['G04a', 10, 6, 'circle'], ['G04G', 11, 6, 'rectangle'], ['G04c', 10, 5, 'circle'], ['G04d', 11, 5, 'circle'],
    ['G05a', 13, 6, 'circle'], ['G05G', 14, 6, 'rectangle'], ['G05c', 13, 5, 'circle'], ['G05d', 14, 5, 'circle'],
    ['G06a', 16, 6, 'circle'], ['G06G', 17, 6, 'rectangle'], ['G06c', 16, 5, 'circle'], ['G06d', 17, 5, 'circle'],
    ['G07a', 19, 6, 'circle'], ['G07G', 20, 6, 'rectangle'], ['G07c', 19, 5, 'circle'], ['G07d', 20, 5, 'circle'],
    ['G08a', 22, 6, 'circle'], ['G08G', 23, 6, 'rectangle'], ['G08c', 22, 5, 'circle'], ['G08d', 23, 5, 'circle'],
    ['G09a', 25, 6, 'circle'], ['G09G', 26, 6, 'rectangle'], ['G09c', 25, 5, 'circle'], ['G09d', 26, 5, 'circle'],
    ['G10a', 28, 6, 'circle'], ['G10G', 29, 6, 'rectangle'], ['G10c', 28, 5, 'circle'], ['G10d', 29, 5, 'circle'],
    ['G11a', 31, 6, 'circle'], ['G11G', 32, 6, 'rectangle'], ['G11c', 31, 5, 'circle'], ['G11d', 32, 5, 'circle'],
    ['G12a', 34, 6, 'circle'], ['G12G', 35, 6, 'rectangle'], ['G12c', 34, 5, 'circle'], ['G12d', 35, 5, 'circle'],

    ['H01a', 1, 3, 'circle'], ['H01H', 2, 3, 'rectangle'], ['H01c', 1, 2, 'circle'], ['H01d', 2, 2, 'circle'],
    ['H02a', 4, 3, 'circle'], ['H02H', 5, 3, 'rectangle'], ['H02c', 4, 2, 'circle'], ['H02d', 5, 2, 'circle'],
    ['H03a', 7, 3, 'circle'], ['H03H', 8, 3, 'rectangle'], ['H03c', 7, 2, 'circle'], ['H03d', 8, 2, 'circle'],
    ['H04a', 10, 3, 'circle'], ['H04H', 11, 3, 'rectangle'], ['H04c', 10, 2, 'circle'], ['H04d', 11, 2, 'circle'],
    ['H05a', 13, 3, 'circle'], ['H05H', 14, 3, 'rectangle'], ['H05c', 13, 2, 'circle'], ['H05d', 14, 2, 'circle'],
    ['H06a', 16, 3, 'circle'], ['H06H', 17, 3, 'rectangle'], ['H06c', 16, 2, 'circle'], ['H06d', 17, 2, 'circle'],
    ['H07a', 19, 3, 'circle'], ['H07H', 20, 3, 'rectangle'], ['H07c', 19, 2, 'circle'], ['H07d', 20, 2, 'circle'],
    ['H08a', 22, 3, 'circle'], ['H08H', 23, 3, 'rectangle'], ['H08c', 22, 2, 'circle'], ['H08d', 23, 2, 'circle'],
    ['H09a', 25, 3, 'circle'], ['H09H', 26, 3, 'rectangle'], ['H09c', 25, 2, 'circle'], ['H09d', 26, 2, 'circle'],
    ['H10a', 28, 3, 'circle'], ['H10H', 29, 3, 'rectangle'], ['H10c', 28, 2, 'circle'], ['H10d', 29, 2, 'circle'],
    ['H11a', 31, 3, 'circle'], ['H11H', 32, 3, 'rectangle'], ['H11c', 31, 2, 'circle'], ['H11d', 32, 2, 'circle'],
    ['H12a', 34, 3, 'circle'], ['H12H', 35, 3, 'rectangle'], ['H12c', 34, 2, 'circle'], ['H12d', 35, 2, 'circle']

    ]
    return coordinates

def shifter_csv_header():
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

def read_shifter_csv_file(shifter_csv):
    for line in open(shifter_csv):
        if line.startswith(';'):
            continue
        PlateType = re.split(r'[ ,;]+', line)[0]
        PlateID = re.split(r'[ ,;]+', line)[1]
        LocationShifter = re.split(r'[ ,;]+', line)[2]
        PlateColumn = '0' * (2 - len(re.split(r'[ ,;]+', line)[3])) + re.split(r'[ ,;]+', line)[3]
        PlateRow = re.split(r'[ ,;]+', line)[4]
        PositionSubWell = re.split(r'[ ,;]+', line)[5]
        Comment = re.split(r'[ ,;]+', line)[6]
        CrystalID = re.split(r'[ ,;]+', line)[7]
        TimeArrival = re.split(r'[ ,;]+', line)[8]
        TimeDeparture = re.split(r'[ ,;]+', line)[9]
        PickDuration = re.split(r'[ ,;]+', line)[10]
        DestinationName = re.split(r'[ ,;]+', line)[11]
        DestinationLocation = re.split(r'[ ,;]+', line)[12]
        Barcode = re.split(r'[ ,;]+', line)[13]
        ExternalComment = re.split(r'[ ,;]+', line)[14]



        well = row + column
        marked_crystal_id = barcode + '-' + well + subwell
        update_marked_crystal_in_db(marked_crystal_id, barcode, well, subwell)
        wellList.append(well + subwell)

def project_description_note():
    msg = (
        'Note: select a project directory; data from existing projects will be read automatically.'
    )
    return msg

def select_project_directory_button_tip():
    msg = (
        'Select a project directory'
    )
    return msg

def crystal_screen_note():
    msg = (
        'Note: crystal screens can be registered either by uploading a manually edited CSV file or'
        ' by uploading a Dragaonfly TXT file. '
        'Hover over the buttons to obtain tooltips with further information.'
    )
    return msg

def add_screen_button_tip():
    msg = (
        'Enter name of the new screen (avoid spaces).\n'
        'and add the name to the dropdown below.\n'
        'Screen name will be used when you save\n'
        'the Crystal Screen to the datavbase '
    )
    return msg

def refresh_screen_button_tip():
    msg = (
        'Loads existing Crystal Screen NAMES from database'
    )
    return msg

def load_selected_screen_button_tip():
    msg = (
        'Loads selected Crystal Screen from database'
    )
    return msg

def save_screen_csv_button_tip(crystal_screen_folder, crystal_screen_template):
    msg = (
        'Saves an empty CSV crystal screen template into\n'
        + str(crystal_screen_folder) + '\n' 
        'Filename is the same as the currently selected screen:\n'
        + crystal_screen_template + '.csv'
    )
    return msg
