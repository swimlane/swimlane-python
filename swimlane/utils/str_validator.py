def validate_str(value, key):
  if not isinstance(value, str):
    raise ValueError('{} must be a string value.'.format(key))
  if value.strip() == '':
    raise ValueError('{} must not be an empty string value.'.format(key))