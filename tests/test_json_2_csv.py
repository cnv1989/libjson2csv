import unittest

from libjson2csv.json_2_csv import reduce_item


class TestJson2Csv(unittest.TestCase):

    def test_reduce_item(self):
        sample_dict = {
            'key_1_1': 'val_1_1_1',
            'key_1_2': [
                'val_1_2_1',
                'val_1_2_2',
                'val_1_2_3'
            ],
            'key_1_3': [{
                'key_1_3_2_1': 'val_1_3_2_1_1'
            }, {
                'key_1_3_2_1': 'val_1_3_2_1_2'
            }, {
                'key_1_3_2_1': 'val_1_3_2_1_3'
            }],
            'key_1_4': {
                'key_1_4_2_1': 'val_1_4_2_1_1'
            },
            'key_1_5': {
                'key_1_5_2_1': [{
                    'key_1_5_2_3_1': 'val_1_5_2_3_1_1'
                }]
            }
        }

        # non minimized
        expected_csv_row = {
            'key_1_1': 'val_1_1_1',
            'key_1_2[0]': 'val_1_2_1',
            'key_1_2[1]': 'val_1_2_2',
            'key_1_2[2]': 'val_1_2_3',
            'key_1_3[0].key_1_3_2_1': 'val_1_3_2_1_1',
            'key_1_3[1].key_1_3_2_1': 'val_1_3_2_1_2',
            'key_1_3[2].key_1_3_2_1': 'val_1_3_2_1_3',
            'key_1_4.key_1_4_2_1': 'val_1_4_2_1_1',
            'key_1_5.key_1_5_2_1[0].key_1_5_2_3_1': 'val_1_5_2_3_1_1'
        }

        csv_row = reduce_item(sample_dict)
        self.assertCountEqual(csv_row.keys(), expected_csv_row.keys())

        # minimized
        expected_csv_row = {
            'key_1_1': 'val_1_1_1',
            '*key_1_2': 'val_1_2_1; val_1_2_2; val_1_2_3',
            'key_1_3[0].key_1_3_2_1': 'val_1_3_2_1_1',
            'key_1_3[1].key_1_3_2_1': 'val_1_3_2_1_2',
            'key_1_3[2].key_1_3_2_1': 'val_1_3_2_1_3',
            'key_1_4.key_1_4_2_1': 'val_1_4_2_1_1',
            'key_1_5.key_1_5_2_1[0].key_1_5_2_3_1': 'val_1_5_2_3_1_1'
        }

        csv_row = reduce_item(sample_dict, minimize_columns=True)
        self.assertCountEqual(csv_row.keys(), expected_csv_row.keys())

    def test_reduce_item_avoid_minimization_if_not_simple_string(self):
        sample_dict = {
            'key_1_1': 'val_1_1_1',
            'key_1_2': [
                'val_1_2_1_1 val_1_2_1_2',
                'val_1_2_2_1',
                'val_1_2_3_1'
            ]
        }

        expected_csv_row = {
            'key_1_1': 'val_1_1_1',
            'key_1_2[0]': 'val_1_2_1 val_1_2_1_2',
            'key_1_2[1]': 'val_1_2_2',
            'key_1_2[2]': 'val_1_2_3'
        }

        csv_row = reduce_item(sample_dict, minimize_columns=True)
        self.assertCountEqual(csv_row.keys(), expected_csv_row.keys())

        sample_dict = {
            'key_1_1': 'val_1_1_1',
            'key_1_2': [
                'val_1_2_1_1;val_1_2_1_2',
                'val_1_2_2_1',
                'val_1_2_3_1'
            ]
        }

        expected_csv_row = {
            'key_1_1': 'val_1_1_1',
            'key_1_2[0]': 'val_1_2_1;val_1_2_1_2',
            'key_1_2[1]': 'val_1_2_2',
            'key_1_2[2]': 'val_1_2_3'
        }

        csv_row = reduce_item(sample_dict, minimize_columns=True)
        self.assertCountEqual(csv_row.keys(), expected_csv_row.keys())
