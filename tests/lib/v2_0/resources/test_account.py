from mock import patch
import json
import httpretty
import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.connect_token import ConnectToken
from contextio.lib.v2_0.helpers import ArgumentError

class TestAccountResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")

    @httpretty.activate
    def test_get_updates_object_with_data_from_api(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://api.context.io/2.0/accounts/fake_id/",
            status=200,
            body=json.dumps({
                "id": "fake_id",
                "username": "fake_username"
            }))

        account = Account(self.contextio, {"id": "fake_id", "username": "wrong_username"})

        account_updated = account.get()

        self.assertTrue(account_updated)
        self.assertEqual("fake_username", account.username)

    @httpretty.activate
    def test_delete_removes_account(self):
        httpretty.register_uri(
            httpretty.DELETE,
            "https://api.context.io/2.0/accounts/fake_id/",
            status=200,
            body=json.dumps({
                "success": True
            }))

        account = Account(self.contextio, {"id": "fake_id"})

        account_deleted = account.delete()

        self.assertTrue(account_deleted)

    @httpretty.activate
    def test_post_updates_account(self):
        httpretty.register_uri(
            httpretty.POST,
            "https://api.context.io/2.0/accounts/fake_id/",
            status=200,
            body=json.dumps({
                "success": True
            }))

        account = Account(self.contextio, {"id": "fake_id"})

        account_updated = account.post(first_name="Leeroy", last_name="Jenkins")

        self.assertTrue(account_updated)
        self.assertEqual(account.first_name, "Leeroy")
        self.assertEqual(account.last_name, "Jenkins")

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

        account = Account(self.contextio, {"id": "fake_id"})

        account_connect_tokens = account.get_connect_tokens()
        connect_token = account_connect_tokens[0]

        self.assertEqual(1, len(account_connect_tokens))
        self.assertIsInstance(connect_token, ConnectToken)
        self.assertIsInstance(connect_token.account, Account)

    @patch("contextio.lib.v2_0.resources.account.Account._request_uri")
    def test_post_connect_token_makes_requires_callback_url(self, mock_request):
        account = Account(self.contextio, {"id": "fake_id"})

        with self.assertRaises(ArgumentError):
            account.post_connect_token()

    @patch("contextio.lib.v2_0.resources.account.Account._request_uri")
    def test_post_connect_token_makes_call_with_correct_params(self, mock_request):
        test_params = {
            "callback_url": "http://some.url",
            "email": "fake@email.com",
            "first_name": "fake",
            "last_name": "name",
            "source_callback_url": "http://some.url",
            "source_sync_all_folders": True,
            "source_sync_flags": "flag",
            "source_raw_file_list": "foo",
            "status_callback_url": "http://some.url",
            "not_valid_param": "not_allowed"
        }

        account = Account(self.contextio, {"id": "fake_id"})
        account.post_connect_token(**test_params)

        del test_params["not_valid_param"]
        mock_request.assert_called_with("connect_tokens", method="POST", params=test_params)
