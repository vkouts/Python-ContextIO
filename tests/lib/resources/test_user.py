from mock import patch
import unittest

from contextio.contextio import ContextIO
from contextio.lib.resources.connect_token import ConnectToken
from contextio.lib.resources.user import User
from contextio.lib.resources.email_account import EmailAccount
from contextio.lib.resources.webhook import WebHook


class TestUser(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar", version="lite")
        self.user = User(self.contextio, {"id": "fake_id"})

    @patch("contextio.lib.resources.base_resource.BaseResource.post")
    def test_post_updates_first_and_last_name(self, mock_post):
        mock_post.return_value = True
        params = {
            "first_name": "Leeroy",
            "last_name": "Jenkins"
        }

        response = self.user.post(**params)

        self.assertEqual(self.user.first_name, "Leeroy")
        self.assertEqual(self.user.last_name, "Jenkins")
        mock_post.assert_called_with(all_args=["first_name", "last_name"], params=params)
        self.assertTrue(response)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_get_connect_tokens_returns_list_of_ConnectTokens(self, mock_request):
        mock_request.return_value = [{"token": "fake_token", "user": {"id": "foobar"}}]

        user_connect_tokens = self.user.get_connect_tokens()

        self.assertEqual(1, len(user_connect_tokens))
        self.assertIsInstance(user_connect_tokens[0], ConnectToken)
        self.assertIsInstance(user_connect_tokens[0].user, User)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_get_email_accounts_returns_list_of_EmailAccounts(self, mock_request):
        mock_request.return_value = [{"label": "fake_label"}]

        user_email_accounts = self.user.get_email_accounts()

        self.assertEqual(1, len(user_email_accounts))
        self.assertIsInstance(user_email_accounts[0], EmailAccount)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_get_webhooks_returns_list_of_WebHooks(self, mock_request):
        mock_request.return_value = [{"webhook_id": "fake_id"}]

        user_webhooks = self.user.get_webhooks()

        self.assertEqual(1, len(user_webhooks))
        self.assertIsInstance(user_webhooks[0], WebHook)

    @patch("contextio.lib.resources.base_resource.BaseResource.post")
    def test_post_webhook_requires_certain_args(self, mock_post):
        mock_post.return_value = {"success": True, "webhook_id": "foobar"}

        req_args = ["callback_url", "failure_notif_url"]
        all_args = [
            "callback_url", "failure_notif_url", "filter_to", "filter_from", "filter_cc",
            "filter_subject", "filter_thread", "filter_new_important", "filter_file_name",
            "filter_folder_added", "filter_folder_removed", "filter_to_domain",
            "filter_from_domain", "include_body", "body_type"
        ]

        self.user.post_webhook()

        mock_post.assert_called_with(
            return_bool=False, all_args=all_args, params={}, required_args=req_args,
            uri="webhooks")

    @patch("contextio.lib.resources.base_resource.BaseResource.post")
    def test_post_webhook_returns_WebHook_object(self, mock_post):
        mock_post.return_value = {"success": True, "webhook_id": "foobar"}
        webhook = self.user.post_webhook()

        self.assertIsInstance(webhook, WebHook)

    @patch("contextio.lib.resources.base_resource.BaseResource.post")
    def test_post_webhook_returns_False_if_creation_failed(self, mock_post):
        mock_post.return_value = {"success": False}
        response = self.user.post_webhook()

        self.assertFalse(response)

