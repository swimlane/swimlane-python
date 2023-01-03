
import validators


class TextFieldType:
    URL = 'url'
    EMAIL = 'email'
    IP = 'ip'
    TELEPHONE = 'telephone'
    TEXT = 'text'


required_error_message = "Required field '{}' is not set"


def validate_text_field_subtype(field):
    field_value = field.get_swimlane()

    if field.input_type == TextFieldType.URL:
        return validate_url(field, field_value)
    elif field.input_type == TextFieldType.EMAIL:
        return validate_email(field, field_value)
    elif field.input_type == TextFieldType.IP:
        return validate_ip(field, field_value)
    elif field.input_type == TextFieldType.TEXT:
        return validate_text(field, field_value)
    else:
        return None


def check_is_required_satisfied(field, value):
    if field.required and not value:
        return False
    if field.required and value:
        return True
    return True


def validate_email(field, field_value):
    is_required_passed = check_is_required_satisfied(field, field_value)
    if not is_required_passed:
        return required_error_message.format(field.name)
    return None if validators.email(field_value) else "The {} is invalid".format(field.name)


def validate_url(field, field_value):
    if not check_is_required_satisfied(field, field_value):
        return required_error_message.format(field.name)
    if isinstance(field_value, str):
        if validators.url(field_value):
            return None
    return "The {} is invalid".format(field.name)


def validate_ip(field, field_value):
    is_required_passed = check_is_required_satisfied(field, field_value)
    if not is_required_passed:
        return required_error_message.format(field.name)
    if isinstance(field_value, str):
        ipv4 = validators.ipv4(field_value)
        ipv6 = validators.ipv6(field_value)
        return None if ipv4 or ipv6 else "The {} is invalid".format(field.name)
    return None


def validate_text(field, field_value):
    is_required_passed = check_is_required_satisfied(field, field_value)
    if not is_required_passed:
        return required_error_message.format(field.name)

    has_min = 'minLength' in field.field_definition
    has_max = 'maxLength' in field.field_definition

    if has_min:
        min_length = field.field_definition['minLength']
    if has_max:
        max_length = field.field_definition['maxLength']

    if not has_min and not has_max and is_required_passed:
        return None

    # has a type because there is a min or max
    length_type = field.field_definition['lengthType']

    if has_min and has_max:
        if length_type == "words":
            if field_value and min_length <= len(field_value.split()) <= max_length:
                return None
            return "The value '{}' does not meet the min({})/max({}) word requirement for field '{}'".format(
                field_value, min_length, max_length, field.name)
        else:
            if field_value and min_length <= len(field_value) <= max_length:
                return None
            return "The value '{}' does not meet the min({})/max({}) character requirement for field '{}'".format(
                field_value, min_length, max_length, field.name)

    if has_min:
        if length_type == "words":
            if field_value and min_length <= len(field_value.split()):
                return None
            return "The value '{}' does not meet the min({}) word requirement for field '{}'".format(field_value,
                                                                                                     min_length,
                                                                                                     field.name)
        else:
            if field_value and min_length <= len(field_value):
                return None
            return "The value '{}' does not meet the min({}) character requirement for field '{}'".format(field_value,
                                                                                                          min_length,
                                                                                                          field.name)

    if has_max:
        if length_type == "words":
            if field_value is None or len(field_value.split()) <= max_length:
                return None
            return "The value '{}' does not meet the max({}) word requirement for field '{}'".format(field_value,
                                                                                                     max_length,
                                                                                                     field.name)
        else:
            if field_value is None or len(field_value) <= max_length:
                return None
            return "The value '{}' does not meet the max({}) character requirement for field '{}'".format(field_value,
                                                                                                          max_length,
                                                                                                          field.name)

    return None
