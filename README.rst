libjson2csv
========

*Converts nested json object to csv and csv back to json*

This package provides functionality to convert valid nested json objects/files to csv and vice versa.

Written in python 3

Usage
-----

To convert json to csv
```
usage: python -m libjson2csv.json_2_csv [--m] <json_in_file_path> [<csv_out_file_path>]
```

To convert csv to json
```
usage: python -m libjson2csv.csv_2_json <csv_in_file_path> [<json_out_file_path>]
```

If the output file path is not provided the output will be dumped to STDOUT.

Specifications
--------------

Scripts expects a valid json.

* JSON can be a valid nested object or a list.
* Script will convert each item of the list to a corresponding row in the csv.
* If JSON is dictionary the outputted csv will contain single row.

Example:

*Converts JSON*

```json
    {
        "key_1_1": "val_1_1_1",
        "key_1_2": [
            "val_1_2_1",
            "val_1_2_2",
            "val_1_2_3"
        ],
        "key_1_3": [{
            "key_1_3_2_1": "val_1_3_2_1_1"
        }, {
            "key_1_3_2_1": "val_1_3_2_1_2"
        }, {
            "key_1_3_2_1": "val_1_3_2_1_3"
        }],
        "key_1_4": {
            "key_1_4_2_1": "val_1_4_2_1_1"
        },
        "key_1_5": {
            "key_1_5_2_1": [{
                "key_1_5_2_3_1": "val_1_5_2_3_1_1"
            }]
        }
    }
```

*TO*

Without `--m` flag

|key_1_1 | key_1_2[0] | key_1_2[1] | key_1_2[2] | key_1_3[0].key_1_3_2_1 | key_1_3[1].key_1_3_2_1 | key_1_3[2].key_1_3_2_1 | key_1_4.key_1_4_2_1 | key_1_5.key_1_5_2_1[0].key_1_5_2_3_1|
|----|----|----|----|----|----|----|----|----|
|val_1_1_1 | val_1_2_1 | val_1_2_2 | val_1_2_3 | val_1_3_2_1_1 | val_1_3_2_1_2 | val_1_3_2_1_3 | val_1_4_2_1_1 | val_1_5_2_3_1_1|

With `--m` flag

|*key_1_2|key_1_1|key_1_3[0].key_1_3_2_1|key_1_3[1].key_1_3_2_1|key_1_3[2].key_1_3_2_1|key_1_4.key_1_4_2_1|key_1_5.key_1_5_2_1[0].key_1_5_2_3_1|
|----|----|----|----|----|----|----|
|val_1_2_1;val_1_2_2;val_1_2_3|val_1_1_1|val_1_3_2_1_1|val_1_3_2_1_2|val_1_3_2_1_3|val_1_4_2_1_1|val_1_5_2_3_1_1|

`--m` stores a simple list in  a single column with items separated by a semicolon.