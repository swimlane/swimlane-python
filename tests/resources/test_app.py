import copy

import pytest

from swimlane.exceptions import UnknownField


def test_repr(mock_app):
    assert repr(mock_app) == '<App: RSA Alerts (RA)>'


def test_get_field_definitions(mock_app):
    """Test retrieving field definitions by name or id and UnknownField error with recommendation"""
    field_def = mock_app.get_field_definition_by_name('Numeric')
    assert field_def['name'] == 'Numeric'

    assert field_def == mock_app.get_field_definition_by_id(field_def['id'])

    # Test UnknownField metadata
    # Suggestions for potential typo
    try:
        mock_app.get_field_definition_by_name('Muneric')
    except UnknownField as error:
        assert error.app is mock_app
        assert error.field_name == 'Muneric'
        assert error.similar_field_names == ['Numeric']
        assert 'Numeric' in str(error)
    else:
        raise RuntimeError

    # Same behavior for get_by_id
    try:
        mock_app.get_field_definition_by_id('aqkf3')
    except UnknownField as error:
        assert error.app is mock_app
        assert error.field_name == 'aqkf3'
        assert error.similar_field_names == ['aqkg3', 'ayqk6', 'aqc6k']
    else:
        raise RuntimeError


def test_resolve_field_name(mock_app):
    """Test that fields keys + names resolve to field name or None if not found"""
    # Field name
    assert mock_app.resolve_field_name('Action') == 'Action'
    # Key
    assert mock_app.resolve_field_name('action-key') == 'Action'
    # Missing
    assert mock_app.resolve_field_name('unknown field name/key') is None


def test_equality(mock_app):
    """Test equality and inequality of Apps by name"""
    app_clone = copy.copy(mock_app)
    assert app_clone == mock_app
    assert not app_clone != mock_app

    app_clone.name = mock_app.name + 'test'
    assert app_clone != mock_app
    assert not app_clone == mock_app


def test_comparison(mock_app, mock_record):
    with pytest.raises(TypeError):
        mock_app < mock_record

    app_clone = copy.copy(mock_app)
    app_clone.name = mock_app.name + 'test'
    assert mock_app < app_clone
    assert app_clone > mock_app
