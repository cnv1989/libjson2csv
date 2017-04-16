import argparse
import csv
import json

# Compatible with both python 2 and python 3
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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


def reduce_json(raw_data, minimize_columns=False):

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


def convert_to_csv(raw_data, output=None, minimize_columns=False):
    if not output:
        output = StringIO()
    headers, processed_data = reduce_json(raw_data, minimize_columns=minimize_columns)
    writer = csv.DictWriter(output, headers)
    writer.writeheader()
    for row in processed_data:
        writer.writerow(row)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='json_2_csv.py',
                                     usage='%(prog)s [--m] <json_in_file> [<csv_out_file>]',
                                     description='Converts json to csv.')

    parser.add_argument('--m', action='store_true')
    parser.add_argument('json_in_file', type=argparse.FileType('r'))
    parser.add_argument('csv_out_file', nargs='?', type=argparse.FileType('w'))

    args = parser.parse_args()

    json_value = args.json_in_file.read()
    raw_data = json.loads(json_value)

    output = convert_to_csv(raw_data, output=args.csv_out_file, minimize_columns=args.m)

    if not args.csv_out_file:
        print(output.getvalue())

    output.close()

    print("Just completed converting to csv.")
