import json
import re


KEY_TYPES = {
    "compound_list": {
        "specifier": "%s[%s]",
        "regex": "^([A-Za-z0-9_-]+)\[([0-9]+)\]$"
    },
    "key": {
        "specifier": "%s",
        "regex": "^([A-Za-z0-9_-]+)$"
    },
    "simple_list": {
        "specifier": "*%s",
        "regex": "^\*([A-Za-z0-9_-]+)$"
    }
}


def to_string(s):
    """Returns a string value of the string"""
    try:
        if type(s) is list:
            '''if a list is provided then the list is joined using ; and converted to string'''
            return ';'.join(map(lambda x: to_string(x), s))
        else:
            return str(s)
    except:
        '''Change the encoding type if needed'''
        return s.encode('utf-8')


def repr_compound_list(key, index):
    """Returns a formatted string that represents a compound list.
    """
    return KEY_TYPES["compound_list"]["specifier"] % (to_string(key), to_string(index))


def repr_key(key):
    """Returns a formatted string that represents a key.
    """
    return KEY_TYPES["key"]["specifier"] % to_string(key)


def repr_simple_list(key):
    """Returns a formatted string that represents a compound list.
    """
    return KEY_TYPES["simple_list"]["specifier"] % to_string(key)


def is_simple_string(element):
    """Return True if the element is a simple string
    simple string is a one word string.
    """
    match = None
    if type(element) == str:
        regex = re.compile("^([A-Za-z0-9_-]+)$")
        match = regex.match(element)
    return True if match else False


def pretty_dump(obj):
    """Returns a indented json dump"""
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))


def is_simple_list(elements):
    """Returns True if the list is a list of numbers or simple strings
    """
    for element in elements:
        if type(element) is not int and \
           type(element) is not float and \
           not is_simple_string(element):
            return False
    return True


def extract_key_and_index(field):
    """Returns the key type, key name and if key is a compound list then returns the index pointed by the field

    Arguments:

    field: csv header field
    """
    for key_type, value in KEY_TYPES.items():
        regex = re.compile(value["regex"])
        match = regex.match(field)
        if match:
            return tuple([key_type] + list(match.groups()))
    return None
