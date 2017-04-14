FORMATTERS = {
    "index": "[%s]",
    "key": ".%s",
    "simple_list": "*%s",
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


def repr_index(x):
    return FORMATTERS["index"] % to_string(x)


def repr_key(x):
    return FORMATTERS["key"] % to_string(x)


def is_simple_list(elements):
    for element in elements:
        if type(element) is not int and type(element) is not str:
            return False
    return True


def repr_simple_list(x):
    return FORMATTERS["simple_list"] % to_string(x)
