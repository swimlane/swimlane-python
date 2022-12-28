import pytest
from swimlane import exceptions

# Not testing the followig field sub-types, because of no format limitations:
# - Telephone
# - Rich text
# - Multi-line text


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'text fields'
    pytest.helpers = helpers
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    yield
    # teardown stuff
    helpers.cleanupData()

def default_valid_fields(email = "valid.email@valid.com", min_max_chars = "minMaxChar", min_chars = "minChars",
                     min_words = "min words ok", min_max_words = "min max words ok", url = "https://www.swimlane.com", ip = "1.1.1.1"):
    return {"Required Text": "required",
     "Email": email,
     "Min Max Chars Text": min_max_chars,
     "Min Chars Text": min_chars,
     "Min Words Text": min_words,
     "Min Max Words Text": min_max_words,
    "url": url,
    "ip": ip
     }


#
# class TestRequiredTextField:
#     def test_required_field(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         assert theRecord["Required Text"] == "required"
#
#     def test_required_field_not_set(helpers):
#         with pytest.raises(exceptions.ValidationError) as excinfo:
#             pytest.app.records.create(**{"Text": "some text"})
#         assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Required field "Required Text" is not set' % pytest.app.acronym
#
#
# class TestUniqueTextField:
#     @pytest.mark.xfail(reason="SPT-6357: API call throws a 500 on the duplicate unique value.")
#     def test_unique_field_duplicate(helpers):
#         uniqueText = "first unique"
#         firstRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Unique Text": uniqueText})
#         assert firstRecord["Unique Text"] == uniqueText
#         # This needs to handle an exception being thrown for the non-unique value
#         pytest.app.records.create(
#             **{"Required Text": "required", "Unique Text": uniqueText})
#
#     @pytest.mark.xfail(reason="SPT-6357: API call throws a 500 on the duplicate unique value.")
#     def test_unique_field_duplicate_on_save(helpers):
#         uniqueText = "second unique"
#         firstRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Unique Text": uniqueText})
#         assert firstRecord["Unique Text"] == uniqueText
#         secondRecord = pytest.app.records.create(
#             **{"Required Text": "required"})
#         secondRecord["Unique Text"] = "second unique"
#         secondRecord.save()
#
#
# class TestCalculatedTextField:
#     def test_calculated_text_field(helpers):
#         textValue = pytest.fake.word()
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Text": textValue})
#         assert theRecord["Calculated Text"] == textValue + "1"
#
#     def test_calculated_text_field_on_save(helpers):
#         textValue = pytest.fake.word()
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Text"] = textValue
#         theRecord.save()
#         assert theRecord["Calculated Text"] == textValue + "1"
#

# TODO Add tests for each when they're required VS when not, which is default and what they're currently doing

class TestEmailTextField:
    @pytest.mark.parametrize("goodEmail", ["valid.email@swimlane.com", "validemail3212@swimlane.net", "totally.valid63@swimlane.co"])
    def test_email_text_field(helpers, goodEmail):
        validFields = default_valid_fields(email=goodEmail)
        theRecord = pytest.app.records.create(
            **validFields)
        assert theRecord["Email"] == goodEmail

    @pytest.mark.parametrize("badEmail", ["invalid.email#swimlane.com", "invalid.email.swimlane.com", "invalid.email@swimlanecom", 123, None, "", ["invalidemail3212@swimlane.net"]])
    def test_invalid_email_on_record_create(helpers, badEmail):
        validFields = default_valid_fields(email=badEmail)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord = pytest.app.records.create(**validFields)
        assert str(excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The Email is invalid]"

# TODO apparently that library is garbage at validating urls, so need to append http/https to those that don't have it to do a proper check
class TestURLTextField:
    @pytest.mark.parametrize("goodUrl", ["swimlane.com", "www.swimlane.com", "http://swimlane.com", "http://www.swimlane.com", "https://swimlane.com", "https://www.swimlane.com",
                                         "swimlane.org", "swimlane.co", "swimlane.io"])
    def test_valid_url_on_record_create(helpers, goodUrl):
        validFields = default_valid_fields(url=goodUrl)
        theRecord = pytest.app.records.create(
            **validFields)
        assert theRecord["URL"] == goodUrl

    @pytest.mark.parametrize("badUrl", ["swimlanecom", "ww.swimlane.com", "http:/swimlane.com", "http//www.swimlane.com",
                              "htps://swimlane.com", "httpswww.swimlane.com",
                              "http://swimlane.", "http//:swimlane.com", "ww.swimlane.co", "swimlane.invalid", 123, None, ""])
    def test_invalid_url_on_record_create(helpers, badUrl):
        invalidUrl = default_valid_fields(url=badUrl)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord = pytest.app.records.create(**invalidUrl)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The URL is invalid]"


class TestIPTextField:
    @pytest.mark.parametrize("goodIp", ["1.1.1.1", "19.117.63.126", "192.168.0.1", "223.255.255.255", "684D:1111:222:3333:4444:5555:6:77",
                                        "2001:db8:3333:4444:5555:6666:1.2.3.4", "::11.22.33.44", "::1234:5678:1.2.3.4"])
    def test_ip_text_field_v4(helpers, goodIp):
        validIp = default_valid_fields(ip=goodIp)
        theRecord = pytest.app.records.create(**validIp)
        assert theRecord["IP"] == goodIp

    @pytest.mark.parametrize("badIp", ["", 123, ""])
    def test_ip_text_field_on_save_v4(helpers, badIp):
        invalidIp = default_valid_fields(ip=badIp)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord = pytest.app.records.create(**invalidIp)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The IP is invalid]"


#
# class TestJSONTextField:
#     # @pytest.mark.xfail(reason="SPT-6362: SHOULD JSON be writable from pydriver??")
#     def test_json_text_field(helpers):
#         textValue = {"a": 1, "b": {"bb": 2}, "c": "hello"}
#         with pytest.raises(exceptions.ValidationError) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "JSON": textValue})
#         assert str(
#             excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Cannot set readonly field \'JSON\'' % pytest.app.acronym
#
#     # @pytest.mark.xfail(reason="SPT-6362: SHOULD JSON be writable from pydriver??")
#     def test_json_text_field_on_save(helpers):
#         textValue = {"a": 1, "b": {"bb": 2}, "c": "hello"}
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         with pytest.raises(exceptions.ValidationError) as excinfo:
#             theRecord['JSON'] = textValue
#         assert str(
#             excinfo.value) == 'Validation failed for <Record: %s>. Reason: Cannot set readonly field \'JSON\'' % theRecord.tracking_id
#
#
# class TestListTextField:
#     def test_list_text_field(helpers):
#         textValue = pytest.fake.pylist(pytest.fake.random_digit(), True, 'str')
#         pytest.app.records.create(
#             **{"Required Text": "required", "Text List": textValue})
#
#     def test_list_text_field_on_save(helpers):
#         textValue = pytest.fake.pylist(pytest.fake.random_digit(), True, 'str')
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord['Text List'] = textValue
#         theRecord.save()
#
#     def test_list_text_field_on_save_reverse(helpers):
#         textValue = pytest.fake.pylist(5, True, 'str')
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Text List": textValue})
#         theRecord['Text List'].reverse()
#         theRecord.save()
#         assert list(theRecord['Text List']) == textValue[::-1]
#
#     def test_list_text_field_on_save_insert(helpers):
#         textValue = pytest.fake.pylist(5, True, 'str')
#         newValue = pytest.fake.word()
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Text List": textValue})
#         theRecord['Text List'].insert(2, newValue)
#         textValue.insert(2, newValue)
#         theRecord.save()
#         assert list(theRecord['Text List']) == textValue
#
#     def test_list_text_field_on_save_insert_bad_value(helpers):
#         textValue = pytest.fake.pylist(5, True, 'str')
#         newValue = 123
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Text List": textValue})
#         with pytest.raises(exceptions.ValidationError) as excinfo:
#             theRecord['Text List'].insert(2, newValue)
#         assert str(excinfo.value) == "Validation failed for <Record: {}>. Reason: Text list field items must be strings, not '<{} 'int'>'".format(
#             theRecord.tracking_id, ("class", "type")[pytest.helpers.py_ver() == 2])
#
#     def test_list_text_field_on_save_append(helpers):
#         textValue = pytest.fake.pylist(5, True, 'str')
#         newValue = pytest.fake.word()
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Text List": textValue})
#         theRecord['Text List'].append(newValue)
#         textValue.append(newValue)
#         theRecord.save()
#         assert list(theRecord['Text List']) == textValue
#
#     def test_list_text_field_on_save_append_bad_value(helpers):
#         textValue = pytest.fake.pylist(5, True, 'str')
#         newValue = 123
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Text List": textValue})
#         with pytest.raises(exceptions.ValidationError) as excinfo:
#             theRecord['Text List'].append(newValue)
#         assert str(excinfo.value) == "Validation failed for <Record: {}>. Reason: Text list field items must be strings, not '<{} 'int'>'".format(
#             theRecord.tracking_id, ("class", "type")[pytest.helpers.py_ver() == 2])
#
#
# class TestMinCharCountTextField:
#     def test_min_char_count_exact(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Chars Text": "abcde"})
#         assert theRecord["Min Chars Text"] == "abcde"
#
#     def test_min_char_count_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Chars Text"] = "abcde"
#         theRecord.save()
#
#     def test_min_char_count_more(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Chars Text": "abcdefghijkl"})
#         assert theRecord["Min Chars Text"] == "abcdefghijkl"
#
#     def test_min_char_count_on_save_more(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Chars Text"] = "abcdefghijkl"
#         theRecord.save()
#
#     def test_min_char_count_too_few(helpers):
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "Min Chars Text": "abcd"})
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Chars Text value of 4 is less than MinLength of 5.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     # Should pyDriver verify before sending API call? YES
#     def test_min_char_count_on_save_too_few(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Chars Text"] = "abcd"
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             theRecord.save()
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Chars Text value of 4 is less than MinLength of 5.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#
# class TestMaxCharCountTextField:
#     def test_max_char_count_exact(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Max Chars Text": "abcdefghij"})
#         assert theRecord["Max Chars Text"] == "abcdefghij"
#
#     def test_max_char_count_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Max Chars Text"] = "abcdefghij"
#         theRecord.save()
#
#     def test_max_char_count_less(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Max Chars Text": "abcde"})
#         assert theRecord["Max Chars Text"] == "abcde"
#
#     def test_max_char_count_on_save_less(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Max Chars Text"] = "abcde"
#         theRecord.save()
#
#     def test_max_char_count_too_many(helpers):
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "Max Chars Text": "abcdefghijk"})
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Max Chars Text value of 11 is higher than MaxLength of 10.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     def test_max_char_count_on_save_too_many(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Max Chars Text"] = "abcdefghijk"
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             theRecord.save()
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Max Chars Text value of 11 is higher than MaxLength of 10.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#
# class TestMinMaxCharCountTextField:
#     def test_min_max_char_count_exact_min(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Max Chars Text": "abcde"})
#         assert theRecord["Min Max Chars Text"] == "abcde"
#
#     def test_min_max_char_count_on_save_exact_min(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Chars Text"] = "abcde"
#         theRecord.save()
#
#     def test_min_max_char_count_exact_max(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Max Chars Text": "abcdefghij"})
#         assert theRecord["Min Max Chars Text"] == "abcdefghij"
#
#     def test_min_max_char_count_on_save_exact_max(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Chars Text"] = "abcdefghij"
#         theRecord.save()
#
#     def test_min_max_char_count_between(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Max Chars Text": "abcdefg"})
#         assert theRecord["Min Max Chars Text"] == "abcdefg"
#
#     def test_min_max_char_count_on_save_between(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Chars Text"] = "abcdefgh"
#         theRecord.save()
#
#     def test_min_max_char_count_too_few(helpers):
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "Min Max Chars Text": "abcd"})
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Max Chars Text value of 4 is less than MinLength of 5.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     # Should pyDriver verify before sending API call?
#     def test_min_max_char_count_on_save_too_few(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Chars Text"] = "abcd"
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             theRecord.save()
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Max Chars Text value of 4 is less than MinLength of 5.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     def test_min_max_char_count_too_many(helpers):
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "Min Max Chars Text": "abcdefghijk"})
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Max Chars Text value of 11 is higher than MaxLength of 10.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     def test_min_max_char_count_on_save_too_many(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Chars Text"] = "abcdefghijk"
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             theRecord.save()
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Max Chars Text value of 11 is higher than MaxLength of 10.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#
# class TestMinWordCountTextField:
#     def test_min_word_count_exact(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Words Text": "hello there how"})
#         assert theRecord["Min Words Text"] == "hello there how"
#
#     def test_min_word_count_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Words Text"] = "hello there how"
#         theRecord.save()
#
#     def test_min_word_count_more(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Words Text": "hello there how are you today"})
#         assert theRecord["Min Words Text"] == "hello there how are you today"
#
#     def test_min_word_count_on_save_more(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Words Text"] = "hello there how are you today"
#         theRecord.save()
#
#     def test_min_word_count_too_few(helpers):
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "Min Words Text": "hello there"})
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Words Text value of 2 is less than MinLength of 3.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     # Should pyDriver verify before sending API call?
#     def test_min_word_count_on_save_too_few(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Words Text"] = "hello there"
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             theRecord.save()
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Words Text value of 2 is less than MinLength of 3.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#
# class TestMaxWordCountTextField:
#     def test_max_word_count_exact(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Max Words Text": "hello there friend how are you doing on this fine"})
#         assert theRecord["Max Words Text"] == "hello there friend how are you doing on this fine"
#
#     def test_max_word_count_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Max Words Text"] = "hello there friend how are you doing on this fine"
#         theRecord.save()
#
#     def test_max_word_count_less(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Max Words Text": "hello there how"})
#         assert theRecord["Max Words Text"] == "hello there how"
#
#     def test_max_word_count_on_save_less(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Max Words Text"] = "hello there how"
#         theRecord.save()
#
#     def test_max_word_count_too_many(helpers):
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "Max Words Text": "hello there friend how are you doing on this fine day"})
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Max Words Text value of 11 is higher than MaxLength of 10.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     def test_max_word_count_on_save_too_many(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Max Words Text"] = "hello there friend how are you doing on this fine day"
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             theRecord.save()
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Max Words Text value of 11 is higher than MaxLength of 10.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#
# class TestMinMaxWordCountTextField:
#     def test_min_max_word_count_exact_min(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Max Words Text": "hello there how"})
#         assert theRecord["Min Max Words Text"] == "hello there how"
#
#     def test_min_max_word_count_on_save_exact_min(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Words Text"] = "hello there how"
#         theRecord.save()
#
#     def test_min_max_word_count_exact_max(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Max Words Text": "hello there friend how are you doing on this fine"})
#         assert theRecord["Min Max Words Text"] == "hello there friend how are you doing on this fine"
#
#     def test_min_max_word_count_on_save_exact_max(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Words Text"] = "hello there friend how are you doing on this fine"
#         theRecord.save()
#
#     def test_min_max_word_count_between(helpers):
#         theRecord = pytest.app.records.create(
#             **{"Required Text": "required", "Min Max Words Text": "hello there friend how are you doing"})
#         assert theRecord["Min Max Words Text"] == "hello there friend how are you doing"
#
#     def test_min_max_word_count_on_save_between(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Words Text"] = "hello there friend how are you"
#         theRecord.save()
#
#     def test_min_max_word_count_too_few(helpers):
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "Min Max Words Text": "hello there"})
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Max Words Text value of 2 is less than MinLength of 3.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     # Should pyDriver verify before sending API call?
#     def test_min_max_word_count_on_save_too_few(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Words Text"] = "hello there"
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             theRecord.save()
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Max Words Text value of 2 is less than MinLength of 3.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     def test_min_max_word_count_too_many(helpers):
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             pytest.app.records.create(
#                 **{"Required Text": "required", "Min Max Words Text": "hello there friend how are you doing on this fine day"})
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Max Words Text value of 11 is higher than MaxLength of 10.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#     def test_min_max_word_count_on_save_too_many(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         theRecord["Min Max Words Text"] = "hello there friend how are you doing on this fine day"
#         with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
#             theRecord.save()
#         assert str(excinfo.value) == 'ModelValidationError:5008 (Field Min Max Words Text value of 11 is higher than MaxLength of 10.): Bad Request for url: %s/api/app/%s/record' % (pytest.helpers.url, pytest.app.id)
#
#
# class TestCommentTextField:
#     def test_comment_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = pytest.fake.sentence()
#         comments = theRecord["Comments"]
#         comments.comment(commentText)
#         theRecord.save()
#         editedRecord = pytest.app.records.get(id=theRecord.id)
#         assert editedRecord['Comments'][-1].message == commentText
#         assert editedRecord['Comments'][-1].is_rich_text == False
#
#     def test_comment_empty_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = ""
#         comments = theRecord["Comments"]
#         comments.comment(commentText)
#         theRecord.save()
#         editedRecord = pytest.app.records.get(id=theRecord.id)
#         assert editedRecord['Comments'][-1].message == commentText
#         assert editedRecord['Comments'][-1].is_rich_text == False
#
#     def test_comment_null_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = None
#         comments = theRecord["Comments"]
#         comments.comment(commentText)
#         theRecord.save()
#         editedRecord = pytest.app.records.get(id=theRecord.id)
#         assert editedRecord['Comments'][-1].message == 'None'
#         assert editedRecord['Comments'][-1].is_rich_text == False
#
#     def test_comment_numeric_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = 1234
#         comments = theRecord["Comments"]
#         comments.comment(commentText)
#         theRecord.save()
#         editedRecord = pytest.app.records.get(id=theRecord.id)
#         assert editedRecord['Comments'][-1].message == '1234'
#         assert editedRecord['Comments'][-1].is_rich_text == False
#
#     def test_comment_json_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = {'comment': 'hello'}
#         comments = theRecord["Comments"]
#         comments.comment(commentText)
#         theRecord.save()
#         editedRecord = pytest.app.records.get(id=theRecord.id)
#         assert editedRecord['Comments'][-1].message == str(commentText)
#         assert editedRecord['Comments'][-1].is_rich_text == False
#
#     def test_comment_object_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = theRecord
#         comments = theRecord["Comments"]
#         comments.comment(commentText)
#         theRecord.save()
#         editedRecord = pytest.app.records.get(id=theRecord.id)
#         assert editedRecord['Comments'][-1].message == str(commentText)
#         assert editedRecord['Comments'][-1].is_rich_text == False
#
#     def test_comment_rich_text_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = pytest.fake.sentence()
#         comments = theRecord["Comments"]
#         comments.comment(commentText, rich_text=True)
#         theRecord.save()
#         editedRecord = pytest.app.records.get(id=theRecord.id)
#         assert editedRecord['Comments'][-1].message == commentText
#         assert editedRecord['Comments'][-1].is_rich_text == True
#
#     def test_comment_rich_text_false_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = pytest.fake.sentence()
#         comments = theRecord["Comments"]
#         comments.comment(commentText, rich_text=False)
#         theRecord.save()
#         editedRecord = pytest.app.records.get(id=theRecord.id)
#         assert editedRecord['Comments'][-1].message == commentText
#         assert editedRecord['Comments'][-1].is_rich_text == False
#
#     def test_comment_rich_text_not_bool_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         commentText = pytest.fake.sentence()
#         comments = theRecord["Comments"]
#         with pytest.raises(ValueError) as excinfo:
#             comments.comment(commentText, rich_text="blah")
#         assert str(excinfo.value) == "rich_text must be a boolean value."
#
#     def test_comment_no_comment_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         comments = theRecord["Comments"]
#         with pytest.raises(TypeError) as excinfo:
#             comments.comment()
#         assert str(excinfo.value) == 'comment() {}'.format(
#             pytest.helpers.py_ver_missing_param(2, 1, "message", "at least"))
#
#     def test_comment_no_comment_rich_text_on_save_exact(helpers):
#         theRecord = pytest.app.records.create(**{"Required Text": "required"})
#         comments = theRecord["Comments"]
#         with pytest.raises(TypeError) as excinfo:
#             comments.comment(rich_text=True)
#         assert str(excinfo.value) == 'comment() {}'.format(
#             pytest.helpers.py_ver_missing_param(2, 2, "message", "at least"))
