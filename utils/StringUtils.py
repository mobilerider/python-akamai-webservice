def lower_case_underscore_to_camel_case(string, ufirst=False):
    """Convert string or unicode from lower-case underscore to camel-case"""
    splitted_string = string.split('_')
    # use string's class to work on the string to keep its type
    class_ = string.__class__
    if ufirst:
        return splitted_string[0] + class_.join('', map(class_.capitalize, splitted_string[1:]))
    else:
        return class_.join('', map(class_.capitalize, splitted_string))