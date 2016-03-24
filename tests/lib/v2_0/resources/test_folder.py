import json
from mock import patch
import httpretty
import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.folder import Folder
from contextio.lib.v2_0.resources.message import Message
from contextio.lib.v2_0.resources.source import Source


class TestFolder(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.account = Account(self.contextio, {"id": "fake_id"})
        self.source = Source(self.account, {"label": "foobar"})

        self.folder = Folder(self.source, {"name": "fake_folder_name"})
        self.uri = "https://api.context.io/2.0/accounts/fake_id/sources/foobar/folders/fake_folder_name/"

    def test_constructor_creates_folder_object_with_all_attributes_in_keys_list(self):
        self.assertTrue(hasattr(self.folder, "name"))
        self.assertTrue(hasattr(self.folder, "attributes"))
        self.assertTrue(hasattr(self.folder, "delim"))
        self.assertTrue(hasattr(self.folder, "nb_messages"))
        self.assertTrue(hasattr(self.folder, "nb_unseen_messages"))

    @httpretty.activate
    def test_get_updates_the_folder_object_with_current_data(self):
        httpretty.register_uri(
            httpretty.GET, self.uri, status=200,
            body=json.dumps({
                "name": "fake_folder_name",
                "nb_messages": 1
            })
        )

        self.assertIsNone(self.folder.nb_messages)
        folder_updated = self.folder.get()

        self.assertTrue(folder_updated)
        self.assertEqual(1, self.folder.nb_messages)

    @httpretty.activate
    def test_put_sends_params_and_returns_True(self):
        httpretty.register_uri(
            httpretty.PUT, self.uri, status=200,
            body=json.dumps({
                "success": True
            })
        )

        created_folder = self.folder.put(delim="foobar")

        request_params = httpretty.last_request().querystring

        self.assertEqual(["foobar"], request_params["delim"])
        self.assertTrue(created_folder)

    @httpretty.activate
    def test_delete_returns_true_if_success(self):
        httpretty.register_uri(
            httpretty.DELETE, self.uri,
            status=200,
            body=json.dumps({
                "success": True
            })
        )

        deleted_folder = self.folder.delete()

        self.assertTrue(deleted_folder)

    @httpretty.activate
    def test_get_updates_attributes_and_returns_True(self):
        httpretty.register_uri(
            httpretty.GET, self.uri + "messages",
            status=200,
            body=json.dumps([
                {"message_id": "fake_id"}
            ])
        )

        messages = self.folder.get_messages()

        self.assertEqual(1, len(messages))
        self.assertIsInstance(messages[0], Message)

    @httpretty.activate
    @patch("contextio.lib.v2_0.helpers.sanitize_params")
    def test_get_messages_sanitizes_params(self, mock_sanitize):
        httpretty.register_uri(
            httpretty.GET, self.uri + "messages",
            status=200,
            body=json.dumps([
                {"message_id": "fake_id"}
            ])
        )

        mock_sanitize.return_value = {}
        self.folder.get_messages(include_body=True)

        mock_sanitize.assert_called_with({'include_body': True}, [
            "include_thread_size", "include_body", "body_type", "include_headers",
            "include_flags", "flag_seen", "limit", "offset" ])

    @httpretty.activate
    def test_get_messages_returns_list_of_Messages(self):
        httpretty.register_uri(
            httpretty.GET, self.uri + "messages",
            status=200,
            body=json.dumps([
                {"message_id": "fake_id"}
            ])
        )

        messages = self.folder.get_messages()

        self.assertEqual(1, len(messages))
        self.assertIsInstance(messages[0], Message)
