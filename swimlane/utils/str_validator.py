def validate_str(value, key):
  if not isinstance(value, str):
    raise ValueError('{} must be a string value.'.format(key))
  if value.strip() == '':
    raise ValueError('{} must not be an empty string value.'.format(key))

def validate_str_format(value, key):
  not_allowed = "@#$%^&*()"
  if any(ch in not_allowed for ch in value):
    raise ValueError('{} is not of the proper format.'.format(key))