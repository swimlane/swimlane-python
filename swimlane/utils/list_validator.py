def validate_str_list(value, key):
    if not value or not isinstance(value, list):
        raise ValueError('{} must be a non-empty list value'.format(key))
    
    for i in value:
        if not isinstance(i, str) or i.strip() == '':
            raise ValueError('{} must contain non-empty string values'.format(key))