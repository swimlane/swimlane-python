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
    if field.required and not value:
        return False
    if field.required and value:
        return True
    return True
    # if field.required and value:
    #     return len(value) > 0
    # return True


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
    #TODO add http scheme to those without it to get it past validation
    if isinstance(fieldValue, str):
        # validDomain = validators.domain(fieldValue)
        validUrl = validators.url(fieldValue)
        if validUrl:
            return None
    return "The {} is invalid".format(field.name)


def validate_ip(field, fieldValue):
    isRequiredPassed = check_is_required_satisfied(field, fieldValue)
    if not isRequiredPassed:
        return requiredErrorMessage.format(field.name)
    if isinstance(fieldValue, str):
        ipv4 = validators.ipv4(fieldValue)
        ipv6 = validators.ipv6(fieldValue)
        return None if ipv4 or ipv6 else "The {} is invalid".format(field.name)
    return None


def validate_text(field, fieldValue):
    # notRequired = check_is_required_satisfied(field, fieldValue)
    # if notRequired:
    #     return None
    isRequiredPassed = check_is_required_satisfied(field, fieldValue)
    hasMin = 'minLength' in field.field_definition
    hasMax = 'maxLength' in field.field_definition

    if hasMin:
        minLength = field.field_definition['minLength']
    if hasMax:
        maxLength = field.field_definition['maxLength']

    if not hasMin and not hasMax and isRequiredPassed:
        return None

    # has a type because there is a min or max
    lengthType = field.field_definition['lengthType']

    if hasMin and hasMax:
        if lengthType == "words":
            if fieldValue and minLength <= len(fieldValue.split()) <= maxLength:
                return None
            return "The value '{}' does not meet the min({})/max({}) word requirement for field '{}'".format(
                fieldValue, minLength, maxLength, field.name)
        else:
            if fieldValue and minLength <= len(fieldValue) <= maxLength:
                return None
            return "The value '{}' does not meet the min({})/max({}) character requirement for field '{}'".format(
                fieldValue, minLength, maxLength, field.name)

    if hasMin:
        if lengthType == "words":
            if fieldValue and minLength <= len(fieldValue.split()):
                return None
            return "The value '{}' does not meet the min({}) word requirement for field '{}'".format(fieldValue,
                                                                                                     minLength,
                                                                                                     field.name)
        else:
            if fieldValue and minLength <= len(fieldValue):
                return None
            return "The value '{}' does not meet the min({}) character requirement for field '{}'".format(fieldValue,
                                                                                                          minLength,
                                                                                                          field.name)

    if hasMax:
        if lengthType == "words":
            if fieldValue is None or len(fieldValue.split()) <= maxLength:
                return None
            return "The value '{}' does not meet the max({}) word requirement for field '{}'".format(fieldValue,
                                                                                                     maxLength,
                                                                                                     field.name)
        else:
            if fieldValue is None or len(fieldValue) <= maxLength:
                return None
            return "The value '{}' does not meet the max({}) character requirement for field '{}'".format(fieldValue,
                                                                                                          maxLength,
                                                                                                          field.name)

    return isRequiredPassed

################## Max only setting can be empty if not required

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

