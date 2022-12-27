import validators


class TextFieldType:
    URL = 'url'
    EMAIL = 'email'
    IP = 'ip'
    TELEPHONE = 'telephone'
    TEXT = 'text'


requiredErrorMessage = "The required field '{}' cannot be empty"


def validate_text_field_subtype(field):
    fieldValue = field.get_swimlane()

    if field.input_type == TextFieldType.URL:
        return validate_url(field, fieldValue)
    elif field.input_type == TextFieldType.EMAIL:
        return validate_email(field, fieldValue)
    elif field.input_type == TextFieldType.IP:
        return validate_ip(field, fieldValue)
    elif field.input_type == TextFieldType.TEXT:
        return validate_text(field, fieldValue)
    else:
        return None


def check_is_required_satisfied(field, value):
    if field.required:
        return len(value) > 0
    return True


def validate_email(field, fieldValue):
    isRequiredPassed = check_is_required_satisfied(field, fieldValue)
    if not isRequiredPassed:
        return requiredErrorMessage.format(field.name)
    return None if validators.email(fieldValue) else "The {} is invalid".format(field.name)


# still is validating ww.google.com for domain
def validate_url(field, fieldValue):
    isRequiredPassed = check_is_required_satisfied(field, fieldValue)
    if not isRequiredPassed:
        return requiredErrorMessage.format(field.name)

    validDomain = validators.domain(fieldValue)
    validUrl = validators.url(fieldValue)
    if validUrl or validDomain:
        return None
    return "The {} is invalid".format(field.name)


def validate_ip(field, fieldValue):
    isRequiredPassed = check_is_required_satisfied(field, fieldValue)
    if not isRequiredPassed:
        return requiredErrorMessage.format(field.name)
    return None if validators.ipv4(fieldValue) else "The {} is invalid".format(field.name)


def validate_text(field, fieldValue):
    hasMin = 'minLength' in field.field_definition
    hasMax = 'maxLength' in field.field_definition

    if hasMin:
        minLength = field.field_definition['minLength']
    if hasMax:
        maxLength = field.field_definition['maxLength']

    if not hasMin and not hasMax and check_is_required_satisfied(field, fieldValue):
        return None

    # has a type because there is a min or max
    lengthType = field.field_definition['lengthType']

    if hasMin and hasMax:
        if lengthType == "words":
            numberOfWords = len(fieldValue.split())
            if minLength <= numberOfWords <= maxLength:
                return None
            return "The value '{}' does not meet the min({})/max({}) word requirement for field '{}'".format(fieldValue,
                                                                                                             minLength,
                                                                                                             maxLength,
                                                                                                             field.name)
        else:
            numberOfCharacters = len(fieldValue)
            if minLength <= numberOfCharacters <= maxLength:
                return None
            return "The value '{}' does not meet the min({})/max({}) character requirement for field '{}'".format(
                fieldValue, minLength, maxLength, field.name)

    if hasMin:
        if lengthType == "words":
            numberOfWords = len(fieldValue.split())
            if minLength <= numberOfWords:
                return None
            return "The value '{}' does not meet the min({}) word requirement for field '{}'".format(fieldValue,
                                                                                                     minLength,
                                                                                                     field.name)
        else:
            numberOfCharacters = len(fieldValue)
            if minLength <= numberOfCharacters:
                return None
            return "The value '{}' does not meet the min({}) character requirement for field '{}'".format(fieldValue,
                                                                                                          minLength,
                                                                                                          field.name)

    if hasMax:
        if lengthType == "words":
            numberOfWords = len(fieldValue.split())
            if numberOfWords <= maxLength:
                return None
            return "The value '{}' does not meet the max({}) word requirement for field '{}'".format(fieldValue,
                                                                                                     maxLength,
                                                                                                     field.name)
        else:
            numberOfCharacters = len(fieldValue)
            if numberOfCharacters <= maxLength:
                return None
            return "The value '{}' does not meet the max({}) character requirement for field '{}'".format(fieldValue,
                                                                                                          maxLength,
                                                                                                          field.name)

    return check_is_required_satisfied(field, fieldValue)


def check_field_min_max(field, fieldValue):
    hasMin = 'minLength' in field.field_definition
    hasMax = 'maxLength' in field.field_definition

    if hasMin:
        minLength = field.field_definition['minLength']
    if hasMax:
        maxLength = field.field_definition['maxLength']

    if not hasMin and not hasMax and check_is_required_satisfied(field, fieldValue):
        return None

    # has a type because there is a min or max
    lengthType = field.field_definition['lengthType']

    if hasMin and hasMax:
        if lengthType == "words":
            numberOfWords = len(fieldValue.split())
            if minLength <= numberOfWords <= maxLength:
                return None
            return "The value '{}' does not meet the min({})/max({}) word requirement for field '{}'".format(fieldValue,
                                                                                                             minLength,
                                                                                                             maxLength,
                                                                                                             field.name)
        else:
            numberOfCharacters = len(fieldValue)
            if minLength <= numberOfCharacters <= maxLength:
                return None
            return "The value '{}' does not meet the min({})/max({}) character requirement for field '{}'".format(
                fieldValue, minLength, maxLength, field.name)

    if hasMin:
        if lengthType == "words":
            numberOfWords = len(fieldValue.split())
            if minLength <= numberOfWords:
                return None
            return "The value '{}' does not meet the min({}) word requirement for field '{}'".format(fieldValue,
                                                                                                     minLength,
                                                                                                     field.name)
        else:
            numberOfCharacters = len(fieldValue)
            if minLength <= numberOfCharacters:
                return None
            return "The value '{}' does not meet the min({}) character requirement for field '{}'".format(fieldValue,
                                                                                                          minLength,
                                                                                                          field.name)

    if hasMax:
        if lengthType == "words":
            numberOfWords = len(fieldValue.split())
            if numberOfWords <= maxLength:
                return None
            return "The value '{}' does not meet the max({}) word requirement for field '{}'".format(fieldValue,
                                                                                                     maxLength,
                                                                                                     field.name)
        else:
            numberOfCharacters = len(fieldValue)
            if numberOfCharacters <= maxLength:
                return None
            return "The value '{}' does not meet the max({}) character requirement for field '{}'".format(fieldValue,
                                                                                                          maxLength,
                                                                                                          field.name)

    return check_is_required_satisfied(field, fieldValue)

