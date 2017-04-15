import re


FORMATS = {
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
    try:
        if type(s) is list:
            return ';'.join(map(lambda x: to_string(x), s))
        else:
            return str(s)
    except:
        # Change the encoding type if needed
        return s.encode('utf-8')


def repr_compound_list(key, index):
    return FORMATS["compound_list"]["specifier"] % (to_string(key), to_string(index))


def repr_key(key):
    return FORMATS["key"]["specifier"] % to_string(key)


def is_simple_list(elements):
    for element in elements:
        if type(element) is not int and \
           type(element) is not str and \
           type(element) is not float:
            return False
    return True


def repr_simple_list(key):
    return FORMATS["simple_list"]["specifier"] % to_string(key)


def extract_key_and_index(key):
    for key_type, value in FORMATS.items():
        regex = re.compile(value["regex"])
        match = regex.match(key)
        if match:
            return tuple([key_type] + list(match.groups()))
    return None
