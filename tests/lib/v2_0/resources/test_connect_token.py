import json
import httpretty
from mock import Mock
import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.connect_token import ConnectToken

class TestConnectToken(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.account = Account(self.contextio, {"id": "fake_id"})

    def test_constructor_creates_account_object_if_account_is_string(self):
        definition = {
            "token": "fake_token",
            "email": "fake@email.com",
            "created": 1458569718,
            "used": 1458569718,
            "expires": False,
            "callback_url": "https://some.url",
            "first_name": "fake",
            "last_name": "name",
            "account": "fake_account_id"
        }

        connect_token = ConnectToken(self.account, definition)

        self.assertIsInstance(connect_token.account, Account)

    def test_constructor_sets_account_attribute_to_none_if_empty_dict(self):
        definition = {
            "token": "fake_token",
            "email": "fake@email.com",
            "created": 1458569718,
            "used": 1458569718,
            "expires": False,
            "callback_url": "https://some.url",
            "first_name": "fake",
            "last_name": "name",
            "account": {}
        }

        account = Account(Mock(), {"id": "fake_id"})
        connect_token = ConnectToken(account, definition)

        self.assertEqual(None, connect_token.account)


    def test_constructor_sets_attributes_on_object(self):
        definition = {
            "token": "fake_token",
            "email": "fake@email.com",
            "created": 1458569718,
            "used": 1458569718,
            "expires": False,
            "callback_url": "https://some.url",
            "first_name": "fake",
            "last_name": "name",
            "account": {
                "id": "fake_account_id"
            }
        }

        connect_token = ConnectToken(Mock(), definition)

        self.assertEqual("fake_token", connect_token.token)
        self.assertEqual("fake@email.com", connect_token.email)
        self.assertEqual(1458569718, connect_token.created)
        self.assertEqual(1458569718, connect_token.used)
        self.assertEqual(False, connect_token.expires)
        self.assertEqual("https://some.url", connect_token.callback_url)
        self.assertEqual("fake", connect_token.first_name)
        self.assertEqual("name", connect_token.last_name)
        self.assertIsInstance(connect_token.account, Account)

    @httpretty.activate
    def test_get_updates_object_with_data_from_api(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://api.context.io/2.0/accounts/fake_id/connect_tokens/fake_token/",
            status=200,
            body=json.dumps({
                "token": "fake_token",
                "email": "fake@email.com"
            }))


        connect_token = ConnectToken(self.account, {
            "token": "fake_token",
            "email": "fake@email.co.uk"
        })

        connect_token_updated = connect_token.get()

        self.assertTrue(connect_token_updated)
        self.assertEqual("fake@email.com", connect_token.email)

    @httpretty.activate
    def test_delete_returns_True_if_success(self):
        httpretty.register_uri(
            httpretty.DELETE,
            "https://api.context.io/2.0/accounts/fake_id/connect_tokens/fake_token/",
            status=200,
            body=json.dumps({
                "success": True
            }))

        connect_token = ConnectToken(self.account, {
            "token": "fake_token",
            "email": "fake@email.co.uk"
        })

        connect_token_deleted = connect_token.delete()

        self.assertTrue(connect_token_deleted)
