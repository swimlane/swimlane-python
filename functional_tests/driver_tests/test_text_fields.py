import pytest
from swimlane import exceptions


# Not testing the following field sub-types, because of no format limitations:
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


def default_valid_fields(email="valid.email@valid.com", min_max_chars="minMaxChar", min_chars="minChars",
                         max_chars="maxChars",
                         min_words="min words ok", max_words="max words ok", min_max_words="min max words ok",
                         url="https://www.swimlane.com",
                         ip="1.1.1.1", text=pytest.fake.word(), required="required",
                         text_list=pytest.fake.pylist(5, True, 'str')):
    return {
        "Required Text": required,
        "Email": email,
        "Min Max Chars Text": min_max_chars,
        "Min Chars Text": min_chars,
        "Max Chars Text": max_chars,
        "Min Words Text": min_words,
        "Max Words Text": max_words,
        "Min Max Words Text": min_max_words,
        "url": url,
        "ip": ip,
        "Text": text,
        "Text List": text_list
    }


class TestRequiredTextField:
    def test_required_field(helpers):
        valid_fields = default_valid_fields(required="this is required")
        the_record = pytest.app.records.create(**valid_fields)
        assert the_record["Required Text"] == "this is required"

    def test_required_field_not_set(helpers):
        valid_fields = default_valid_fields(required=None)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(**valid_fields)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [Required field 'Required Text' is not set]"


class TestUniqueTextField:
    @pytest.mark.xfail(reason="SPT-6357: API call throws a 500 on the duplicate unique value.")
    def test_unique_field_duplicate(helpers):
        uniqueText = "first unique"
        firstRecord = pytest.app.records.create(
            **{"Required Text": "required", "Unique Text": uniqueText})
        assert firstRecord["Unique Text"] == uniqueText
        # This needs to handle an exception being thrown for the non-unique value
        pytest.app.records.create(
            **{"Required Text": "required", "Unique Text": uniqueText})

    @pytest.mark.xfail(reason="SPT-6357: API call throws a 500 on the duplicate unique value.")
    def test_unique_field_duplicate_on_save(helpers):
        uniqueText = "second unique"
        firstRecord = pytest.app.records.create(
            **{"Required Text": "required", "Unique Text": uniqueText})
        assert firstRecord["Unique Text"] == uniqueText
        secondRecord = pytest.app.records.create(
            **{"Required Text": "required"})
        secondRecord["Unique Text"] = "second unique"
        secondRecord.save()


class TestCalculatedTextField:
    def test_calculated_text_field(helpers):
        initialText = pytest.fake.word()
        valid_fields = default_valid_fields(text=initialText)
        the_record = pytest.app.records.create(**valid_fields)
        assert the_record["Calculated Text"] == initialText + "1"

    def test_calculated_text_field_on_save(helpers):
        initialText = pytest.fake.word()
        valid_fields = default_valid_fields(text=initialText)
        the_record = pytest.app.records.create(**valid_fields)
        the_record["Text"] = initialText
        the_record.save()
        assert the_record["Calculated Text"] == initialText + "1"


class TestEmailTextField:
    @pytest.mark.parametrize("goodEmail",
                             ["valid.email@swimlane.com", "validemail3212@swimlane.net", "totally.valid63@swimlane.co"])
    def test_email_text_field_valid(helpers, goodEmail):
        valid_fields = default_valid_fields(email=goodEmail)
        the_record = pytest.app.records.create(
            **valid_fields)
        assert the_record["Email"] == goodEmail

    @pytest.mark.parametrize("goodEmail",
                             ["valid.email@swimlane.com", "validemail3212@swimlane.net", "totally.valid63@swimlane.co"])
    def test_max_char_count_on_save_success(helpers, goodEmail):
        valid_fields = default_valid_fields(email=goodEmail)
        the_record = pytest.app.records.create(**valid_fields)
        the_record["Email"] = goodEmail
        the_record.save()

    @pytest.mark.parametrize("badEmail",
                             ["invalid.email#swimlane.com", "invalid.email.swimlane.com", "invalid.email@swimlanecom",
                              123, None, "", ["invalidemail3212@swimlane.net"]])
    def test_invalid_email_on_record_create(helpers, badEmail):
        valid_fields = default_valid_fields(email=badEmail)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**valid_fields)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The Email is invalid]"


class TestURLTextField:
    @pytest.mark.parametrize("goodUrl", ["http://swimlane.com", "http://www.swimlane.com", "https://swimlane.com",
                                         "https://www.swimlane.com", "https://www.swimlane.io", "http://swimlane.biz"])
    def test_url_text_field_valid(helpers, goodUrl):
        valid_fields = default_valid_fields(url=goodUrl)
        the_record = pytest.app.records.create(
            **valid_fields)
        assert the_record["URL"] == goodUrl

    @pytest.mark.parametrize("goodUrl", ["http://swimlane.com", "http://www.swimlane.com", "https://swimlane.com",
                                         "https://www.swimlane.com", "https://www.swimlane.io", "http://swimlane.biz"])
    def test_url_text_field_valid_on_save(helpers, goodUrl):
        valid_fields = default_valid_fields(url=goodUrl)
        the_record = pytest.app.records.create(**valid_fields)
        the_record["URL"] = goodUrl
        the_record.save()

    @pytest.mark.parametrize("badUrl", ["swimlane.com", "www.swimlane.com", "swimlanecom", "ww.swimlane.com",
                                        "http:/swimlane.com", "http//www.swimlane.com",
                                        "htps://swimlane.com", "httpswww.swimlane.com",
                                        "http://swimlane.", "http//:swimlane.com", "ww.swimlane.co", "swimlane.invalid",
                                        "http://swimlane_com", 123, None, ""])
    def test_url_text_field_invalid(helpers, badUrl):
        invalidUrl = default_valid_fields(url=badUrl)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**invalidUrl)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The URL is invalid]"


class TestIPTextField:
    @pytest.mark.parametrize("goodIp", ["1.1.1.1", "19.117.63.126", "192.168.0.1", "223.255.255.255",
                                        "684D:1111:222:3333:4444:5555:6:77",
                                        "2001:db8:3333:4444:5555:6666:1.2.3.4", "::11.22.33.44", "::1234:5678:1.2.3.4"])
    def test_ip_text_field_valid(helpers, goodIp):
        validIp = default_valid_fields(ip=goodIp)
        the_record = pytest.app.records.create(**validIp)
        assert the_record["IP"] == goodIp

    @pytest.mark.parametrize("goodIp", ["1.1.1.1", "19.117.63.126", "192.168.0.1", "223.255.255.255",
                                        "684D:1111:222:3333:4444:5555:6:77",
                                        "2001:db8:3333:4444:5555:6666:1.2.3.4", "::11.22.33.44", "::1234:5678:1.2.3.4"])
    def test_ip_text_field_on_save_success(helpers, goodIp):
        validIp = default_valid_fields(ip=goodIp)
        the_record = pytest.app.records.create(**validIp)
        the_record["IP"] = goodIp
        the_record.save()

    @pytest.mark.parametrize("badIp",
                             ["101", 123, "1.1", "ipAddress", "www.swimlane.com", "192.158.1.", "92.158.1.321"])
    def test_ip_text_field_invalid(helpers, badIp):
        invalidIp = default_valid_fields(ip=badIp)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**invalidIp)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The IP is invalid]"


class TestJSONTextField:
    # @pytest.mark.xfail(reason="SPT-6362: SHOULD JSON be writable from pydriver??")
    def test_json_text_field(helpers):
        textValue = {"a": 1, "b": {"bb": 2}, "c": "hello"}
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Text": "required", "JSON": textValue})
        assert str(
            excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Cannot set readonly field \'JSON\'' % pytest.app.acronym

    # @pytest.mark.xfail(reason="SPT-6362: SHOULD JSON be writable from pydriver??")
    def test_json_text_field_on_save(helpers):
        textValue = {"a": 1, "b": {"bb": 2}, "c": "hello"}
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record['JSON'] = textValue
        assert str(
            excinfo.value) == 'Validation failed for <Record: %s>. Reason: Cannot set readonly field \'JSON\'' % the_record.tracking_id


class TestListTextField:
    def test_list_text_field(helpers):
        textValue = pytest.fake.pylist(pytest.fake.random_digit(), True, 'str')
        valid_fields = default_valid_fields(text_list=textValue)
        pytest.app.records.create(**valid_fields)

    def test_list_text_field_on_save(helpers):
        textValue = pytest.fake.pylist(pytest.fake.random_digit(), True, 'str')
        valid_fields = default_valid_fields(text_list=textValue)
        the_record = pytest.app.records.create(**valid_fields)
        the_record['Text List'] = textValue
        the_record.save()

    def test_list_text_field_on_save_reverse(helpers):
        textValue = pytest.fake.pylist(pytest.fake.random_digit(), True, 'str')
        valid_fields = default_valid_fields(text_list=textValue)
        the_record = pytest.app.records.create(**valid_fields)
        the_record['Text List'].reverse()
        the_record.save()
        assert list(the_record['Text List']) == textValue[::-1]

    def test_list_text_field_on_save_insert(helpers):
        textValue = pytest.fake.pylist(5, True, 'str')
        valid_fields = default_valid_fields(text_list=textValue)
        newValue = pytest.fake.word()
        the_record = pytest.app.records.create(**valid_fields)
        the_record['Text List'].insert(2, newValue)
        textValue.insert(2, newValue)
        the_record.save()
        assert list(the_record['Text List']) == textValue

    def test_list_text_field_on_save_insert_bad_value(helpers):
        textValue = pytest.fake.pylist(5, True, 'str')
        valid_fields = default_valid_fields(text_list=textValue)
        newValue = 123
        the_record = pytest.app.records.create(**valid_fields)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record['Text List'].insert(2, newValue)
        assert str(
            excinfo.value) == "Validation failed for <Record: {}>. Reason: Text list field items must be strings, not '<{} 'int'>'".format(
            the_record.tracking_id, ("class", "type")[pytest.helpers.py_ver() == 2])

    def test_list_text_field_on_save_append(helpers):
        textValue = pytest.fake.pylist(5, True, 'str')
        valid_fields = default_valid_fields(text_list=textValue)
        newValue = pytest.fake.word()
        the_record = pytest.app.records.create(**valid_fields)
        the_record['Text List'].append(newValue)
        textValue.append(newValue)
        the_record.save()
        assert list(the_record['Text List']) == textValue

    def test_list_text_field_on_save_append_bad_value(helpers):
        textValue = pytest.fake.pylist(5, True, 'str')
        valid_fields = default_valid_fields(text_list=textValue)
        newValue = 123
        the_record = pytest.app.records.create(**valid_fields)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record['Text List'].append(newValue)
        assert str(
            excinfo.value) == "Validation failed for <Record: {}>. Reason: Text list field items must be strings, not '<{} 'int'>'".format(
            the_record.tracking_id, ("class", "type")[pytest.helpers.py_ver() == 2])


class TestMinCharCountTextField:
    @pytest.mark.parametrize("goodMinCharCount", ["validChar", "valid", "verylongstringwithlotsofcharacters"])
    def test_min_char_count_valid(helpers, goodMinCharCount):
        validMinCharCount = default_valid_fields(min_chars=goodMinCharCount)
        the_record = pytest.app.records.create(**validMinCharCount)
        assert the_record["Min Chars Text"] == goodMinCharCount

    @pytest.mark.parametrize("goodMinCharCount", ["validChar", "valid", "verylongstringwithlotsofcharacters"])
    def test_min_char_count_on_save_success(helpers, goodMinCharCount):
        validMinCharCount = default_valid_fields(min_chars=goodMinCharCount)
        the_record = pytest.app.records.create(**validMinCharCount)
        the_record["Min Chars Text"] = goodMinCharCount
        the_record.save()

    @pytest.mark.parametrize("badMinCharCount", ["v", "four", "cat", "hi", None, 123])
    def test_min_char_count_invalid(helpers, badMinCharCount):
        invalidMinCharCount = default_valid_fields(min_chars=badMinCharCount)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**invalidMinCharCount)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The value '{}' does not meet the min(5) character requirement for field 'Min Chars Text']".format(
            badMinCharCount)


class TestMaxCharCountTextField:
    @pytest.mark.parametrize("goodMaxCharCount", ["v", "four", "cat", "hi", "", None, 123])
    def test_max_char_count_valid(helpers, goodMaxCharCount):
        validMaxCharCount = default_valid_fields(max_chars=goodMaxCharCount)
        the_record = pytest.app.records.create(**validMaxCharCount)
        if isinstance(goodMaxCharCount, str):
            assert the_record["Max Chars Text"] == goodMaxCharCount

    @pytest.mark.parametrize("goodMaxCharCount", ["v", "four", "cat", "hi", "", None, 123])
    def test_max_char_count_on_save_success(helpers, goodMaxCharCount):
        validMaxCharCount = default_valid_fields(max_chars=goodMaxCharCount)
        the_record = pytest.app.records.create(**validMaxCharCount)
        the_record["Max Chars Text"] = goodMaxCharCount
        the_record.save()

    @pytest.mark.parametrize("badMaxCharCount", ["toomanycharacters", "hihihihihihi", 1234567891011])
    def test_max_char_count_invalid(helpers, badMaxCharCount):
        invalidMaxCharCount = default_valid_fields(max_chars=badMaxCharCount)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**invalidMaxCharCount)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The value '{}' does not meet the max(10) character requirement for field 'Max Chars Text']".format(
            badMaxCharCount)


class TestMinMaxCharCountTextField:
    @pytest.mark.parametrize("goodMinMaxCharCount", ["inbetween", "hello", 1234567])
    def test_min_max_char_count_valid(helpers, goodMinMaxCharCount):
        validMinMaxCharCount = default_valid_fields(min_max_chars=goodMinMaxCharCount)
        the_record = pytest.app.records.create(**validMinMaxCharCount)
        if isinstance(goodMinMaxCharCount, str):
            assert the_record["Min Max Chars Text"] == goodMinMaxCharCount

    @pytest.mark.parametrize("goodMinMaxCharCount", ["inbetween", "hello", 1234567])
    def test_min_max_char_count_on_save_success(helpers, goodMinMaxCharCount):
        validMinMaxCharCount = default_valid_fields(min_max_chars=goodMinMaxCharCount)
        the_record = pytest.app.records.create(**validMinMaxCharCount)
        the_record["Min Max Chars Text"] = goodMinMaxCharCount
        the_record.save()

    @pytest.mark.parametrize("badMinMaxCharCount",
                             ["", "1", "hi", "cat", "fish", "hellohellohello", "toomanycharacters", 123456734534, None])
    def test_min_max_char_count_invalid(helpers, badMinMaxCharCount):
        invalidMinMaxCharCount = default_valid_fields(min_max_chars=badMinMaxCharCount)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**invalidMinMaxCharCount)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The value '{}' does not meet the min(5)/max(10) character requirement for field 'Min Max Chars Text']".format(
            badMinMaxCharCount)


class TestMinWordCountTextField:
    @pytest.mark.parametrize("goodMinWordCount", ["three words enough", "a lot of valid words",
                                                  "a quick brown fox jumped over the lazy log"])
    def test_min_word_count_valid(helpers, goodMinWordCount):
        validMinWordCount = default_valid_fields(min_words=goodMinWordCount)
        the_record = pytest.app.records.create(**validMinWordCount)
        if isinstance(goodMinWordCount, str):
            assert the_record["Min Words Text"] == goodMinWordCount

    @pytest.mark.parametrize("goodMinWordCount", ["three words enough", "a lot of valid words",
                                                  "a quick brown fox jumped over the lazy log"])
    def test_min_word_count_on_save_success(helpers, goodMinWordCount):
        validMinWordCount = default_valid_fields(min_words=goodMinWordCount)
        the_record = pytest.app.records.create(**validMinWordCount)
        the_record["Min Words Text"] = goodMinWordCount
        the_record.save()

    @pytest.mark.parametrize("badMinWordCount", ["", "one", "not enough", None, 123])
    def test_min_word_count_invalid(helpers, badMinWordCount):
        invalidMinWordCount = default_valid_fields(min_words=badMinWordCount)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**invalidMinWordCount)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The value '{}' does not meet the min(3) word requirement for field 'Min Words Text']".format(
            badMinWordCount)


class TestMaxWordCountTextField:
    @pytest.mark.parametrize("goodMaxWordCount",
                             ["ten words are a valid and will pass the test", "a lot of valid words",
                              "a quick brown fox jumped over the lazy log"])
    def test_max_word_count_valid(helpers, goodMaxWordCount):
        validMaxWordCount = default_valid_fields(max_words=goodMaxWordCount)
        the_record = pytest.app.records.create(**validMaxWordCount)
        if isinstance(goodMaxWordCount, str):
            assert the_record["Max Words Text"] == goodMaxWordCount

    @pytest.mark.parametrize("goodMaxWordCount",
                             ["ten words are a valid and will pass the test", "a lot of valid words",
                              "a quick brown fox jumped over the lazy log"])
    def test_max_word_count_on_save_success(helpers, goodMaxWordCount):
        validMaxWordCount = default_valid_fields(max_words=goodMaxWordCount)
        the_record = pytest.app.records.create(**validMaxWordCount)
        the_record["Max Words Text"] = goodMaxWordCount
        the_record.save()

    @pytest.mark.parametrize("badMaxWordCount", ["eleven words are needed to fail the max words test case",
                                                 "a lot of valid words a lot of valid words a lot of valid words",
                                                 "a very sleepy fox lazed around and never tried to jump over any logs"])
    def test_max_word_count_invalid(helpers, badMaxWordCount):
        invalidMaxWordCount = default_valid_fields(max_words=badMaxWordCount)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**invalidMaxWordCount)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The value '{}' does not meet the max(10) word requirement for field 'Max Words Text']".format(
            badMaxWordCount)


class TestMinMaxWordCountTextField:
    @pytest.mark.parametrize("goodMinMaxWordCount",
                             ["ten words are a valid and will pass the test", "a lot of valid words",
                              "three are enough", "a quick brown fox jumped over the lazy log"])
    def test_min_max_word_count_valid(helpers, goodMinMaxWordCount):
        validMinMaxWordCount = default_valid_fields(min_max_words=goodMinMaxWordCount)
        the_record = pytest.app.records.create(**validMinMaxWordCount)
        if isinstance(goodMinMaxWordCount, str):
            assert the_record["Min Max Words Text"] == goodMinMaxWordCount

    @pytest.mark.parametrize("goodMinMaxWordCount",
                             ["ten words are a valid and will pass the test", "a lot of valid words",
                              "three are enough", "a quick brown fox jumped over the lazy log"])
    def test_min_max_word_count_on_save_success(helpers, goodMinMaxWordCount):
        validMinMaxWordCount = default_valid_fields(min_max_words=goodMinMaxWordCount)
        the_record = pytest.app.records.create(**validMinMaxWordCount)
        the_record["Min Max Words Text"] = goodMinMaxWordCount
        the_record.save()

    @pytest.mark.parametrize("badMinMaxWordCount", ["", "one", "two words", None, 123,
                                                    "eleven words are needed to fail the max words test case",
                                                    "a lot of valid words a lot of valid words a lot of valid words",
                                                    "a very sleepy fox lazed around and never tried to jump over any logs"])
    def test_min_max_word_count_invalid(helpers, badMinMaxWordCount):
        invalidMinMaxWordCount = default_valid_fields(min_max_words=badMinMaxWordCount)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            the_record = pytest.app.records.create(**invalidMinMaxWordCount)
        assert str(
            excinfo.value) == "Validation failed for <Record: WXXX - New>. Reason: The following fields contain errors: [The value '{}' does not meet the min(3)/max(10) word requirement for field 'Min Max Words Text']".format(
            badMinMaxWordCount)


class TestCommentTextField:
    def test_comment_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = pytest.fake.sentence()
        comments = the_record["Comments"]
        comments.comment(commentText)
        the_record.save()
        editedRecord = pytest.app.records.get(id=the_record.id)
        assert editedRecord['Comments'][-1].message == commentText
        assert editedRecord['Comments'][-1].is_rich_text == False

    def test_comment_empty_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = ""
        comments = the_record["Comments"]
        comments.comment(commentText)
        the_record.save()
        editedRecord = pytest.app.records.get(id=the_record.id)
        assert editedRecord['Comments'][-1].message == commentText
        assert editedRecord['Comments'][-1].is_rich_text == False

    def test_comment_null_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = None
        comments = the_record["Comments"]
        comments.comment(commentText)
        the_record.save()
        editedRecord = pytest.app.records.get(id=the_record.id)
        assert editedRecord['Comments'][-1].message == 'None'
        assert editedRecord['Comments'][-1].is_rich_text == False

    def test_comment_numeric_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = 1234
        comments = the_record["Comments"]
        comments.comment(commentText)
        the_record.save()
        editedRecord = pytest.app.records.get(id=the_record.id)
        assert editedRecord['Comments'][-1].message == '1234'
        assert editedRecord['Comments'][-1].is_rich_text == False

    def test_comment_json_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = {'comment': 'hello'}
        comments = the_record["Comments"]
        comments.comment(commentText)
        the_record.save()
        editedRecord = pytest.app.records.get(id=the_record.id)
        assert editedRecord['Comments'][-1].message == str(commentText)
        assert editedRecord['Comments'][-1].is_rich_text == False

    def test_comment_object_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = the_record
        comments = the_record["Comments"]
        comments.comment(commentText)
        the_record.save()
        editedRecord = pytest.app.records.get(id=the_record.id)
        assert editedRecord['Comments'][-1].message == str(commentText)
        assert editedRecord['Comments'][-1].is_rich_text == False

    def test_comment_rich_text_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = pytest.fake.sentence()
        comments = the_record["Comments"]
        comments.comment(commentText, rich_text=True)
        the_record.save()
        editedRecord = pytest.app.records.get(id=the_record.id)
        assert editedRecord['Comments'][-1].message == commentText
        assert editedRecord['Comments'][-1].is_rich_text == True

    def test_comment_rich_text_false_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = pytest.fake.sentence()
        comments = the_record["Comments"]
        comments.comment(commentText, rich_text=False)
        the_record.save()
        editedRecord = pytest.app.records.get(id=the_record.id)
        assert editedRecord['Comments'][-1].message == commentText
        assert editedRecord['Comments'][-1].is_rich_text == False

    def test_comment_rich_text_not_bool_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        commentText = pytest.fake.sentence()
        comments = the_record["Comments"]
        with pytest.raises(ValueError) as excinfo:
            comments.comment(commentText, rich_text="blah")
        assert str(excinfo.value) == "rich_text must be a boolean value."

    def test_comment_no_comment_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        comments = the_record["Comments"]
        with pytest.raises(TypeError) as excinfo:
            comments.comment()
        assert str(excinfo.value) == 'comment() {}'.format(
            pytest.helpers.py_ver_missing_param(2, 1, "message", "at least"))

    def test_comment_no_comment_rich_text_on_save_exact(helpers):
        valid_fields = default_valid_fields()
        the_record = pytest.app.records.create(**valid_fields)
        comments = the_record["Comments"]
        with pytest.raises(TypeError) as excinfo:
            comments.comment(rich_text=True)
        assert str(excinfo.value) == 'comment() {}'.format(
            pytest.helpers.py_ver_missing_param(2, 2, "message", "at least"))
