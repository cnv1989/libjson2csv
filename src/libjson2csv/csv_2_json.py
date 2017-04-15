import argparse
import csv

from copy import deepcopy
from .utils import extract_key_and_index
from .utils import pretty_dump


def get_object_in_dict(dictionary, keys_list):
    """Returns the value from the dictionary

    Arguments:

    dictionary -- dictionary from which the value is retrieved.
    keys_list -- nested keys represented in the form of a list.
    """
    value = dictionary  # starting location is always the dictionary itself.
    for key in keys_list:
        key_index_info = extract_key_and_index(key)
        key_type = key_index_info[0]
        key_name = key_index_info[1]
        if key_type == 'key' or key_type == 'simple_list':
            value = value[key_name]
        elif key_type == 'compound_list':
            key_index = int(key_index_info[2])
            if type(value[key_name]) is list:
                value = value[key_name][key_index]
            else:
                raise TypeError("cannot get element at index %s for type %s" % (key_index,
                                                                                type(value[key_name])))
    return value


def add_or_update_key_in_dict(dictionary, keys_list, level=-1, value=None):
    """Returns the updated copy of the dictionary

    Arguments:

    dictionary -- dictionary to which new key is to be added.
    keys_list -- nested keys represented in the form of a list.

    Keyword arguments:

    level -- nested level of key in keys_list that should be added or updated in the dictionary (default = -1 # last element)
    value -- default value of the terminal key. (default = None)
    """
    dictionary = deepcopy(dictionary)  # make a copy of the dictionary to avoid changing the state of the original dictionary

    is_terminal_key = False

    if level == len(keys_list) - 1 or level == -1:
        is_terminal_key = True

    if not is_terminal_key and value:
        raise ValueError('Value cannot be set on non terminal keys')

    '''get the reference to the dictionary that holds the key within the nesting'''
    current_location = get_object_in_dict(dictionary, keys_list[:level])
    key_index_info = extract_key_and_index(keys_list[level])

    key_type = key_index_info[0]
    key_name = key_index_info[1]

    if key_type == 'key':
        if is_terminal_key:
            current_location[key_name] = value
        else:
            '''if key is not a terminal key then it must be a dictionary'''
            current_location[key_name] = {}

    elif key_type == 'simple_list':
        if not is_terminal_key:
            raise KeyError('simple list key type must be a terminal key')
        current_location[key_name] = []
        if value:
            current_location[key_name] = value.split(';')

    elif key_type == 'compound_list':
        key_index = int(key_index_info[2])

        '''if the dictionary doesn't contain the key then initialize it'''
        if key_name not in current_location:
            current_location[key_name] = []

        curr_list = current_location[key_name]
        if key_index < len(curr_list):
            current_location[key_name][level] = value if is_terminal_key else {}
        else:
            current_list = current_location[key_name]
            '''if the index exceeds the size of compound list then expand the list.'''
            for index in range(len(current_list), key_index):
                current_list.append(None if is_terminal_key else {})
            current_list.append(value if is_terminal_key else {})

    return dictionary


def create_schema_dict_from_fieldnames(fieldnames):
    """Initializes and returns a dictionary representing the schema of the json dict using the fieldnames

    Arguments:

    fieldnames -- list of all the header fields in the csv.
    """
    schema_dict = {}
    keys_list_info = []
    '''Intermediate list to keep track of the level in the key list that is being  processed'''
    for field in fieldnames:
        keys = field.split('.')
        keys_list_info.append({
            'keys': keys,
            'level': 0
        })

    '''Loops over all the keys in list one level at a time.'''
    while True:
        processed_keys = 0
        for row in range(len(keys_list_info)):
            keys_info = keys_list_info[row]
            if keys_info.get('level') < len(keys_info['keys']):
                schema_dict = add_or_update_key_in_dict(schema_dict, keys_info['keys'], level=keys_info.get('level'))
                processed_keys += 1
                keys_info['level'] += 1
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


def row_contains_data(fieldnames, row):
    """Returns True if the value of atleast on of the fields is truthy"""
    for field in fieldnames:
        if row.get(field):
            return True
    return False


def convert_to_json(csv_reader):
    fieldnames = csv_reader.fieldnames
    schema_dict = create_schema_dict_from_fieldnames(fieldnames)
    json_list = []
    for row in csv_reader:
        if row_contains_data(fieldnames, row):
            json_list.append(get_json_for_row(row, fieldnames, schema_dict))

    return json_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='csv_2_json.py',
                                     usage='%(prog)s <csv_in_file_path> <json_out_file_path>',
                                     description='Converts csv to json')

    parser.add_argument('csv_in_file_path', type=str)
    parser.add_argument('json_out_file_path', type=str)

    args = parser.parse_args()

    with open(args.csv_in_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = convert_to_json(csv_reader)

        with open(args.json_out_file_path, 'w') as json_file:
            json_file.write(pretty_dump(json_data))

    print("Just completed writing the json file")
