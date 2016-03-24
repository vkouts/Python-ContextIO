import json
import httpretty
from mock import Mock, patch
import unittest

from contextio.lib.v2_0.resources.base_resource import BaseResource

def create_mock_resource(parent=Mock(), initialize_mock=Mock()):

    class MockResource(BaseResource):
        keys = ['id', 'foo', 'baz']

        def __init__(self, parent, definition):
            self.parent = parent

            initialize_mock(parent, definition)
            super(MockResource, self).__init__(parent, "/some-uri/{id}", definition)

        def _request_uri(self, *args, **kwargs):
            return super(MockResource, self)._request_uri("test/")


    return MockResource(parent, {"id": "fake_id", "foo": "bar"})

class TestBaseResource(unittest.TestCase):
    @patch("contextio.lib.v2_0.resources.base_resource.logging.error")
    def test_constructor_logs_error_if_definition_is_empty_string(self, mock_logging_error):
        BaseResource(Mock(), "/some-uri", "")

        mock_logging_error.assert_called_with("Empty response received for /some-uri")

    @patch("contextio.lib.v2_0.resources.base_resource.helpers.uncamelize")
    @patch("contextio.lib.v2_0.resources.base_resource.logging.error")
    def test_constructor_logs_error_if_definition_is_empty_string(self, mock_logging_error, mock_uncamelize):
        mock_uncamelize.side_effect = Exception
        BaseResource(Mock(), "/some-uri", {"foo": "bar"})

        mock_logging_error.assert_called_with("Invalid response received for /some-uri")


    def test_constructor_sets_attributes_from_class_keys_and_definition(self):
        mock_parent = Mock()
        mock_resource = create_mock_resource(mock_parent)

        self.assertEqual("fake_id", mock_resource.id)
        self.assertEqual("bar", mock_resource.foo)
        self.assertIsNone(mock_resource.baz)
        self.assertEqual(mock_parent, mock_resource.parent)
        self.assertEqual("/some-uri/fake_id", mock_resource.base_uri)

    def test_uri_for_joins_arguments_with_base_uri(self):
        mock_resource = create_mock_resource()
        uri = mock_resource._uri_for('some','other-resource')

        self.assertEqual("/some-uri/fake_id/some/other-resource", uri)

    def test_get_calls_init_on_itself_with_its_parent_object_and_request_result_as_arguments(self):
        mock_parent = Mock()
        mock_init = Mock()
        mock_parent._request_uri.return_value = {"id": "fake_id", "foo": "bar"}

        mock_resource = create_mock_resource(parent=mock_parent, initialize_mock=mock_init)

        response = mock_resource.get(mock_parent)

        mock_init.assert_called_with(mock_parent, {"id": "fake_id", "foo": "bar"})
        self.assertTrue(response)

    def test_delete_sends_delete_request_to_resource_base_uri(self):
        mock_parent = Mock()
        mock_parent._request_uri.return_value = {
            "success": True
        }
        mock_resource = create_mock_resource(parent=mock_parent)

        response = mock_resource.delete()

        self.assertTrue(response)
