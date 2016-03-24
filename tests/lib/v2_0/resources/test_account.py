from mock import patch
import json
import httpretty
import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.connect_token import ConnectToken
from contextio.lib.v2_0.resources.email_address import EmailAddress
from contextio.lib.v2_0.resources.message import Message
from contextio.lib.v2_0.resources.source import Source
from contextio.lib.v2_0.resources.thread import Thread
from contextio.lib.v2_0.resources.webhook import WebHook
from contextio.lib.v2_0.resources.file import File
from contextio.lib.v2_0.helpers import ArgumentError

class TestAccountResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.account = Account(self.contextio, {"id": "fake_id"})

        self.uri = "https://api.context.io/2.0/accounts/fake_id/"
    @httpretty.activate
    def test_post_updates_first_and_last_name(self):
        httpretty.register_uri(
            httpretty.POST,
            "https://api.context.io/2.0/accounts/fake_id/",
            status=200,
            body=json.dumps({
                "success": True
            }))

        account_updated = self.account.post(first_name="Leeroy", last_name="Jenkins")

        self.assertTrue(account_updated)
        self.assertEqual(self.account.first_name, "Leeroy")
        self.assertEqual(self.account.last_name, "Jenkins")

    @httpretty.activate
    def test_get_connect_tokens_returns_list_of_connect_tokens(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://api.context.io/2.0/accounts/fake_id/connect_tokens",
            status=200,
            body=json.dumps([
                {
                    "token": "fake_token",
                    "email": "fake@email.com",
                    "created": 1458569698,
                    "used": 1458569718,
                    "serverLabel": "server.label",
                    "callback_url": "https://some.url",
                    "first_name": "Fake",
                    "last_name": "Name",
                    "expires": False,
                    "account" : {
                        "id": "fake_account_id"
                    }
                }
            ])
        )


        account_connect_tokens = self.account.get_connect_tokens()
        connect_token = account_connect_tokens[0]

        self.assertEqual(1, len(account_connect_tokens))
        self.assertIsInstance(connect_token, ConnectToken)
        self.assertIsInstance(connect_token.account, Account)

    @httpretty.activate
    def test_get_contacts_returns_list_of_contacts(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://api.context.io/2.0/accounts/fake_id/connect_tokens",
            status=200,
            body=json.dumps([
                {
                    "token": "fake_token",
                    "email": "fake@email.com",
                    "created": 1458569698,
                    "used": 1458569718,
                    "serverLabel": "server.label",
                    "callback_url": "https://some.url",
                    "first_name": "Fake",
                    "last_name": "Name",
                    "expires": False,
                    "account" : {
                        "id": "fake_account_id"
                    }
                }
            ])
        )


        account_connect_tokens = self.account.get_connect_tokens()
        connect_token = account_connect_tokens[0]

        self.assertEqual(1, len(account_connect_tokens))
        self.assertIsInstance(connect_token, ConnectToken)
        self.assertIsInstance(connect_token.account, Account)

    @httpretty.activate
    def test_get_email_addresses_returns_list_of_EmailAddresses(self):
        httpretty.register_uri(httpretty.GET, self.uri+ "email_addresses", status=200,
            body=json.dumps([{"email": "fake_token"}]))

        response = self.account.get_email_addresses()

        self.assertIsInstance(response[0], EmailAddress)

    @httpretty.activate
    def test_get_files_returns_list_of_Files(self):
        httpretty.register_uri(httpretty.GET, self.uri+ "files", status=200,
            body=json.dumps([{"file_id": "foobar"}]))

        response = self.account.get_files()

        self.assertIsInstance(response[0], File)

    @httpretty.activate
    def test_get_messages_returns_list_of_Messages(self):
        httpretty.register_uri(httpretty.GET, self.uri + "messages", status=200,
            body=json.dumps([{"message_id": "foobar"}]))

        response = self.account.get_messages()

        self.assertIsInstance(response[0], Message)

    @httpretty.activate
    def test_get_sources_returns_list_of_Sources(self):
        httpretty.register_uri(httpretty.GET, self.uri + "sources", status=200,
            body=json.dumps([{"label": "foobar"}]))

        response = self.account.get_sources()

        self.assertIsInstance(response[0], Source)

    @httpretty.activate
    def test_get_sync_returns_a_dictionary(self):
        httpretty.register_uri(httpretty.GET, self.uri + "sync", status=200,
            body=json.dumps({"foo": "bar"}))

        response = self.account.get_sync()

        self.assertIsInstance(response, dict)

    @httpretty.activate
    def test_get_threads_returns_list_of_Threads(self):
        httpretty.register_uri(httpretty.GET, self.uri + "threads", status=200,
            body=json.dumps(["foo/bar"]))

        response = self.account.get_threads()

        self.assertIsInstance(response[0], Thread)

    @httpretty.activate
    def test_get_webhooks_returns_list_of_WebHooks(self):
        httpretty.register_uri(httpretty.GET, self.uri + "webhooks", status=200,
            body=json.dumps([{"webhook_id": "foobar"}]))

        response = self.account.get_webhooks()

        self.assertIsInstance(response[0], WebHook)

    @httpretty.activate
    def test_get_email_addresses_returns_list_of_email_addresses(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://api.context.io/2.0/accounts/fake_id/connect_tokens",
            status=200,
            body=json.dumps([
                {
                    "token": "fake_token",
                    "email": "fake@email.com",
                    "created": 1458569698,
                    "used": 1458569718,
                    "serverLabel": "server.label",
                    "callback_url": "https://some.url",
                    "first_name": "Fake",
                    "last_name": "Name",
                    "expires": False,
                    "account" : {
                        "id": "fake_account_id"
                    }
                }
            ])
        )


        account_connect_tokens = self.account.get_connect_tokens()
        connect_token = account_connect_tokens[0]

        self.assertEqual(1, len(account_connect_tokens))
        self.assertIsInstance(connect_token, ConnectToken)
        self.assertIsInstance(connect_token.account, Account)

    def test_post_connect_token_requires_callback_url(self):
        with self.assertRaises(ArgumentError):
            self.account.post_connect_token()

    def test_post_email_address_requires_email_address(self):
        with self.assertRaises(ArgumentError):
            self.account.post_email_address()

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_email_address_returns_EmailAddress(self, mock_post):
        mock_post.return_value = {"email": "fake@email.com"}

        email_address = self.account.post_email_address(email_address="fake@email.com")

        self.assertIsInstance(email_address, EmailAddress)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_message_requires_certain_args(self, mock_post):
        all_args = [
            "dst_source", "dst_folder", "message", "flag_seen", "flag_answered", "flag_flagged",
            "flag_deleted", "flag_draft"
        ]
        req_args = ["dst_source", "dst_folder", "message"]

        self.account.post_message()

        mock_post.assert_called_with(
            all_args=all_args, headers={"Content-Type": "multipart/form-data"},
            params={},
            required_args=req_args,
            return_bool=False,
            uri="messages")

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_source_requires_certain_args(self, mock_post):
        all_args = [
            'email', 'server', 'username', 'port', 'type', 'use_ssl',
            'origin_ip', 'expunge_on_deleted_flag', 'sync_all_folders',
            'sync_folders', 'sync_flags', 'raw_file_list', 'password',
            'provider_refresh_token', 'provider_consumer_key',
            'callback_url', 'status_callback_url'
        ]
        req_args = ['email', 'server', 'username', 'port', 'type', 'use_ssl']

        self.account.post_source()

        mock_post.assert_called_with(
            return_bool=False,
            all_args=all_args,
            params={"use_ssl": 1, "type": "IMAP", "port": 993},
            required_args=req_args,
            uri="sources")

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_source_returns_Source_object(self, mock_post):
        mock_post.return_value = {"label": "foobar"}
        source = self.account.post_source()

        self.assertIsInstance(source, Source)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_source_returns_False_if_creation_failed(self, mock_post):
        mock_post.return_value = {"success": False}
        response = self.account.post_source()

        self.assertFalse(response)


    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_post_sync_calls_request_uri_with_correct_args(self, mock_request):
        self.account.post_sync()

        mock_request.assert_called_with("sync", method="POST")

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_webhook_requires_certain_args(self, mock_post):
        req_args = ['callback_url', 'failure_notif_url']
        all_args = [
            'callback_url', 'failure_notif_url', 'filter_to', 'filter_from', 'filter_cc',
            'filter_subject', 'filter_thread', 'filter_new_important', 'filter_file_name',
            'filter_folder_added', 'filter_folder_removed', 'filter_to_domain',
            'filter_from_domain', 'include_body', 'body_type', 'include_parsed_receipts'
        ]

        self.account.post_webhook()

        mock_post.assert_called_with(
            return_bool=False,
            all_args=all_args,
            params={},
            required_args=req_args,
            uri="webhooks")

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_webhook_returns_WebHook_object(self, mock_post):
        mock_post.return_value = {"success": True, "webhook_id": "foobar"}
        webhook = self.account.post_webhook()

        self.assertIsInstance(webhook, WebHook)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_webhook_returns_False_if_creation_failed(self, mock_post):
        mock_post.return_value = {"success": False}
        response = self.account.post_webhook()

        self.assertFalse(response)

