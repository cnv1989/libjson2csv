import csv
import json
import sys

from utils import is_simple_list
from utils import repr_index
from utils import repr_key
from utils import repr_simple_list
from utils import to_string


MINIMIZE_COLUMNS = True


def reduce_key(key, value):

    reduced_item = {}

    # When item is a list create multiple columns with
    if type(value) is list:
        if MINIMIZE_COLUMNS and is_simple_list(value):
            reduced_item[repr_simple_list(key)] = to_string(value)
        else:
            i = 0
            for sub_item in value:
                reduced_item.update(reduce_key("%s%s" % (key, repr_index(i)), sub_item))
                i = i + 1

    # Reduction Condition 2
    elif type(value) is dict:
        for sub_key, sub_value in value.items():
            sub_reduced_items = reduce_key(sub_key, sub_value)
            for _key, _value in sub_reduced_items.items():
                reduced_item["%s%s" % (key, repr_key(_key))] = _value

    # Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)

    return reduced_item


def reduce_item(item):
    processed_data = {}
    for key, value in item.items():
        processed_data.update(reduce_key(key, value))
    return processed_data


def convert_to_csv(raw_data):

    data_to_be_processed = raw_data

    if type(raw_data) is not list:
        data_to_be_processed = [raw_data]

    rows = []
    headers = []

    for item in data_to_be_processed:
        row = reduce_item(item)
        rows.append(row)
        headers += row.keys()

    headers = list(set(headers))
    headers.sort()

    return headers, rows


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "\nUsage: python json_to_csv.py <node_name> <json_in_file_path> <csv_out_file_path>\n"
    else:
        # Reading arguments
        json_file_path = sys.argv[2]
        csv_file_path = sys.argv[3]

        fp = open(json_file_path, 'r')
        json_value = fp.read()
        raw_data = json.loads(json_value)
        headers, processed_data = convert_to_csv(raw_data)

        with open(csv_file_path, 'wb+') as f:
            writer = csv.DictWriter(f, headers, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)

        print "Just completed writing csv file with %d columns" % len(headers)
