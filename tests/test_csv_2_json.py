import unittest

from json2csv.csv_2_json import add_or_update_key_in_dict
from json2csv.csv_2_json import create_schema_dict_from_fieldnames
from json2csv.csv_2_json import get_object_in_dict


class TestCsv2Json(unittest.TestCase):

    def test_get_object_in_dict(self):

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
            }
        }

        obj = get_object_in_dict(sample_dict, ['key_1_1'])
        self.assertEqual(obj, sample_dict['key_1_1'])

        obj = get_object_in_dict(sample_dict, ['key_1_2[1]'])
        self.assertEqual(obj, sample_dict['key_1_2'][1])

        obj = get_object_in_dict(sample_dict, ['key_1_3[1]'])
        self.assertEqual(obj, sample_dict['key_1_3'][1])

        obj = get_object_in_dict(sample_dict, ['key_1_3[1]', 'key_1_3_2_1'])
        self.assertEqual(obj, sample_dict['key_1_3'][1]['key_1_3_2_1'])

        obj = get_object_in_dict(sample_dict, ['*key_1_2'])
        self.assertEqual(obj, sample_dict['key_1_2'])

        obj = get_object_in_dict(sample_dict, ['key_1_4', 'key_1_4_2_1'])
        self.assertEqual(obj, sample_dict['key_1_4']['key_1_4_2_1'])

        with self.assertRaises(KeyError):
            get_object_in_dict(sample_dict, ['key_1_5'])

        with self.assertRaises(IndexError):
            get_object_in_dict(sample_dict, ['key_1_2[3]'])

        with self.assertRaises(TypeError):
            get_object_in_dict(sample_dict, ['key_1_1[3]'])

    def test_add_or_update_key_in_dict(self):

        self.assertEqual(add_or_update_key_in_dict({}, ['key_1_1'], value='val_1_1_1'), {
            'key_1_1': 'val_1_1_1'
        })

        self.assertEqual(add_or_update_key_in_dict({}, ['key_1_2[0]'], value='val_1_2_1'), {
            'key_1_2': ['val_1_2_1']
        })

        self.assertEqual(add_or_update_key_in_dict({}, ['key_1_2[1]'], value='val_1_2_1'), {
            'key_1_2': [None, 'val_1_2_1']
        })

        self.assertEqual(add_or_update_key_in_dict({'key_1_1': {}}, ['key_1_1', 'key_1_1_2'], value='val_1_1_2_1'), {
            'key_1_1': {
                'key_1_1_2': 'val_1_1_2_1'
            }
        })

        self.assertEqual(add_or_update_key_in_dict({}, ['key_1_1', 'key_1_1_2'], level=0), {
            'key_1_1': {}
        })

        with self.assertRaises(ValueError):
            add_or_update_key_in_dict({'key_1_1': {}}, ['key_1_1', 'key_1_1_2'], level=0, value='val_1_1_2_1')

        with self.assertRaises(KeyError):
            add_or_update_key_in_dict({}, ['key_1_1', 'key_1_1_2'], value='val_1_1_2_1')

        with self.assertRaises(TypeError):
            add_or_update_key_in_dict({'key_1_1': None}, ['key_1_1', 'key_1_1_2'], value='val_1_1_2_1')

        with self.assertRaises(TypeError):
            add_or_update_key_in_dict({'key_1_1': None}, ['key_1_1', 'key_1_1_2'], value='val_1_1_2_1')

    def test_create_schema_dict_from_fieldnames(self):

        fieldnames = [
            'key_1_1',
            'key_1_2.key_1_2_2_1',
            'key_1_2.key_1_2_2_2',
            'key_1_3.*key_1_3_2_1',
            'key_1_4[1].key_1_4_2_1',
            'key_1_5.key_1_5_2_1.key_1_5_2_3_1'
        ]
        dictionary = create_schema_dict_from_fieldnames(fieldnames)
        expected_dict = {
            'key_1_1': None,
            'key_1_2': {
                'key_1_2_2_1': None,
                'key_1_2_2_2': None
            },
            'key_1_3': {
                'key_1_3_2_1': []
            },
            'key_1_4': [
                {},
                {
                    'key_1_4_2_1': None
                }
            ],
            'key_1_5': {
                'key_1_5_2_1': {
                    'key_1_5_2_3_1': None
                }
            }
        }

        self.assertEqual(dictionary, expected_dict)

    def test_create_schema_dict_from_fieldnames_with_bad_fields(self):
        fieldnames = ['key_1_1', 'key_1_2.*key_1_2_2_1.key_1_2_2_1']

        with self.assertRaises(KeyError):
            create_schema_dict_from_fieldnames(fieldnames)

if __name__ == '__main__':
    unittest.main()
