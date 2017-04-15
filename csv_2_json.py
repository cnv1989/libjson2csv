import sys
import json
import csv

from copy import deepcopy
from .utils import extract_key_and_index


def get_object_in_dict(dictionary, keys_list):
    current_location = dictionary
    for key in keys_list:
        key_index_info = extract_key_and_index(key)
        key_type = key_index_info[0]
        key_name = key_index_info[1]
        if key_type == 'key' or key_type == 'simple_list':
            current_location = current_location[key_name]
        elif key_type == 'compound_list':
            key_index = int(key_index_info[2])
            if type(current_location[key_name]) is list:
                current_location = current_location[key_name][key_index]
            else:
                raise TypeError("cannot get element at index %s for type %s" % (key_index,
                                                                                type(current_location[key_name])))
    return current_location


def add_or_update_key_in_dict(dictionary, keys_list, index=-1, value=None):
    # We create a copy of the dictionary to prevent this method from changing the state of the input dictionary
    dictionary = deepcopy(dictionary)

    is_terminal_key = False

    if index == len(keys_list) - 1 or index == -1:
        is_terminal_key = True

    if not is_terminal_key and value:
        raise ValueError('Value cannot be set on non terminal keys')

    current_location = get_object_in_dict(dictionary, keys_list[:index])
    key_index_info = extract_key_and_index(keys_list[index])

    key_type = key_index_info[0]
    key_name = key_index_info[1]

    if key_type == 'key':
        if is_terminal_key:
            current_location[key_name] = value
        else:
            current_location[key_name] = {}
    elif key_type == 'simple_list':
        if not is_terminal_key:
            raise KeyError('simple list key type must be a terminal key')
        current_location[key_name] = []
        if value:
            current_location[key_name] = value.split(';')

    elif key_type == 'compound_list':
        key_index = int(key_index_info[2])

        if key_name not in current_location:
            current_location[key_name] = []

        curr_list = current_location[key_name]
        if key_index < len(curr_list):
            current_location[key_name][index] = value if is_terminal_key else {}
        else:
            current_list = current_location[key_name]
            for index in range(len(current_list), key_index):
                current_list.append(None if is_terminal_key else {})
            current_list.append(value if is_terminal_key else {})

    return dictionary


def create_schema_dict_from_fieldnames(fieldnames):
    '''
    Creates a schema dict using all the headers
    '''
    schema_dict = {}
    keys_list_info = []

    for field in fieldnames:
        keys = field.split('.')
        keys_list_info.append({
            'keys': keys,
            'index': 0
        })

    while True:
        processed_keys = 0
        for index in range(len(keys_list_info)):
            keys_info = keys_list_info[index]
            if keys_info.get('index') < len(keys_info['keys']):
                schema_dict = add_or_update_key_in_dict(schema_dict, keys_info['keys'], index=keys_info.get('index'))
                processed_keys += 1
                keys_info['index'] += 1
            else:
                continue

        if not processed_keys:
            break

    return schema_dict


def get_json_for_row(row, fieldnames, schema_dict):
    dictionary = deepcopy(schema_dict)
    for field in fieldnames:
        value = row.get(field)
        dictionary = add_or_update_key_in_dict(dictionary, field.split('.'), value=value)

    return dictionary


def convert_to_json(csv_reader):
    fieldnames = csv_reader.fieldnames
    schema_dict = create_schema_dict_from_fieldnames(fieldnames)
    json_list = []
    for row in csv_reader:
        json_list.append(get_json_for_row(row, fieldnames, schema_dict))

    return json_list


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nUsage: python csv_to_json.py <csv_in_file_path> <json_out_file_path>\n")
    else:
        # Reading arguments
        csv_file_path = sys.argv[2]
        json_file_path = sys.argv[3]

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            json_data = convert_to_json(csv_reader)

            with open(json_file_path, 'w') as json_file:
                json_file.write(json.dumps(json_data))

        print("Just completed writing the json file")
