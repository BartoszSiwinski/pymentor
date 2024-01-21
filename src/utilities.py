def get_key_for_value(_dict, val):
    for key, values in _dict.items():
        if val in values:
            return key
    raise "key doesn't exist"
