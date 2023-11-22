import json
import sys
import struct
import os

def signed_byte(b):
    return b - 256 if b >= 128 else b

with open('data/data.json') as json_file:
    DATA = json.loads(json_file.read())

MAGIC = DATA['Magic']

def parse(tbl):

    with open(tbl, 'rb') as tbl_file:
        tbl_data = tbl_file.read()
        print(f'Opening {tbl}...')

    file_name = tbl[4:-4]

    if list(tbl_data)[ : 102] != MAGIC or tbl_data[106] != 4 or tbl_data[-1] != 11:
        print('Error: invalid magic')
        return 0
    
    print('Magic check succeeded')

    #Size
    size = int.from_bytes(tbl_data[102 : 106], byteorder = 'little')
    table_name_size = tbl_data[107]
    table_name = tbl_data[108 : 108 + table_name_size].decode('utf-8')

    print('Reading metadata...')
    
    #Indexes check
    for _ in range(size + 1):
        if int.from_bytes(tbl_data[108 + table_name_size + 5 * _ : 112 + table_name_size + 5 * _], byteorder = 'little') != _ + 2:
            print('Error: index check failed')
            return 0
        
    print('Index check succeeded')

    #Param table
    new_offset = 112 + table_name_size + size * 5
    
    if list(tbl_data[new_offset : new_offset + 5]) != [5, 3, 0, 0, 0] or tbl_data[new_offset + 5] != table_name_size or tbl_data[new_offset + 6 : new_offset + 6 + tbl_data[new_offset + 5]].decode('utf-8') != table_name:
        print('Error: param table header check failed')
        return 0
    
    print('Reading param table...')

    new_offset += 6 + tbl_data[new_offset + 5]
    param_num = int.from_bytes(tbl_data[new_offset : new_offset + 4], byteorder = 'little')
    new_offset += 4
    param_table = []

    for _ in range(param_num):
        param_name_size = tbl_data[new_offset]
        param_name = tbl_data[new_offset + 1 : new_offset + 1 + param_name_size].decode('utf-8')
        new_offset += param_name_size + 1
        param_table.append({'Param name': param_name})

    for _ in range(param_num):
        param_table[_]['Unknown value'] = tbl_data[new_offset]
        new_offset += 1

    for _ in range(param_num):
        param_table[_]['Type'] = tbl_data[new_offset]
        new_offset += 1

    if list(tbl_data[new_offset : new_offset + 4]) != [2, 0, 0, 0]:
        print('Error: param table closer check failed')
        return 0
    
    new_offset += 4

    print('Finished reading param table.')

    #Raw data

    print('Reading raw data...')

    data = []

    for _ in range(size):

        data.append({})

        for param in param_table:

            if param['Type'] == 1:
                value = signed_byte(tbl_data[new_offset])
                plus_offset = 1

            elif param['Type'] == 8:
                value = int.from_bytes(tbl_data[new_offset : new_offset + 4], byteorder = 'little', signed = True)
                plus_offset = 4

            elif param['Type'] == 11:
                value = struct.unpack('f', tbl_data[new_offset : new_offset + 4])[0]
                plus_offset = 4

            data[-1][param['Param name']] = value
            new_offset += plus_offset

        new_offset += 9

    print('Finished reading raw data.')

    with open(f'json/{file_name}.json', 'w') as json_file:
        json_file.write(json.dumps(data, indent = 2))

    print('Converted to json successfully.')

def parse_all():

    for file in os.listdir('tbl'):

        parse('tbl/' + file)

parse_all()