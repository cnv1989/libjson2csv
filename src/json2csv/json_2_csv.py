import argparse
import csv
import json

from .utils import is_simple_list
from .utils import repr_compound_list
from .utils import repr_key
from .utils import repr_simple_list
from .utils import to_string


def reduce_key(key, value, minimize_columns=False):
    """Flattens the value of the key and appends the keys in the value dictionary to parent key.
    """

    reduced_item = {}

    if type(value) is list:
        '''Reduction Condition 1: value of the key is a list'''

        if minimize_columns and is_simple_list(value):
            '''If the value is a simple list i.e. the list is a list of strings or integers, group all the values
            under single column'''
            reduced_item[repr_simple_list(key)] = to_string(value)
        else:
            i = 0
            for sub_item in value:
                '''Create a new column for each of the index in the list.'''
                reduced_item.update(reduce_key("%s" % (repr_compound_list(key, i)), sub_item))
                i = i + 1

    elif type(value) is dict:
        '''Reduction Condition 1: value of the key is a dictionary'''
        for sub_key, sub_value in value.items():
            sub_reduced_items = reduce_key(sub_key, sub_value)
            for _key, _value in sub_reduced_items.items():
                reduced_item["%s.%s" % (key, repr_key(_key))] = _value

    else:
        reduced_item[to_string(key)] = to_string(value)

    return reduced_item


def reduce_item(item, minimize_columns=False):
    """Returns a flat dictionary with keys representing the headers in csv"""
    processed_data = {}
    for key, value in item.items():
        processed_data.update(reduce_key(key, value, minimize_columns=minimize_columns))
    return processed_data


def convert_to_csv(raw_data, minimize_columns=False):

    data_to_be_processed = raw_data

    if type(raw_data) is not list:
        data_to_be_processed = [raw_data]

    rows = []
    headers = []

    for item in data_to_be_processed:
        row = reduce_item(item, minimize_columns=minimize_columns)
        rows.append(row)
        headers += row.keys()

    headers = list(set(headers))
    headers.sort()

    return headers, rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='json_2_csv.py',
                                     usage='%(prog)s [--minimize-columns] <json_in_file_path> <csv_out_file_path>',
                                     description='Converts json to csv.')

    parser.add_argument('--minimize-columns', action='store_true')
    parser.add_argument('json_in_file_path', type=str)
    parser.add_argument('csv_out_file_path', type=str)

    args = parser.parse_args()

    fp = open(args.json_in_file_path, 'r')
    json_value = fp.read()
    raw_data = json.loads(json_value)
    headers, processed_data = convert_to_csv(raw_data, minimize_columns=args.minimize_columns)

    with open(args.csv_out_file_path, 'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in processed_data:
            writer.writerow(row)

    print("Just completed writing csv file with %d columns" % len(headers))
