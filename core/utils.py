def list_to_string(lst):
    return ','.join(map(str, lst))


def string_to_list(string):
    return [int(item) for item in string.split(',') if item]