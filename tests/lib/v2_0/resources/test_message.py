import json
import httpretty
import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.message import Message


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.account = Account(self.contextio, {"id": "fake_id"})

        self.message = Message(self.account, {"message_id": "fake_message_id"})
        self.uri = "https://api.context.io/2.0/accounts/fake_id/messages/fake_message_id/"

    def test_constructor_creates_message_object_with_all_attributes_in_keys_list(self):
        self.assertTrue(hasattr(self.message, 'date'))
        self.assertTrue(hasattr(self.message, 'date_indexed'))
        self.assertTrue(hasattr(self.message, 'addresses'))
        self.assertTrue(hasattr(self.message, 'person_info'))
        self.assertTrue(hasattr(self.message, 'email_message_id'))
        self.assertTrue(hasattr(self.message, 'message_id'))
        self.assertTrue(hasattr(self.message, 'gmail_message_id'))
        self.assertTrue(hasattr(self.message, 'gmail_thread_id'))
        self.assertTrue(hasattr(self.message, 'files'))
        self.assertTrue(hasattr(self.message, 'subject'))
        self.assertTrue(hasattr(self.message, 'folders'))
        self.assertTrue(hasattr(self.message, 'sources'))

    @httpretty.activate
    def test_get_updates_the_message_object_with_current_data_and_returns_True(self):
        httpretty.register_uri(
            httpretty.GET, self.uri, status=200,
            body=json.dumps({
                "message_id": "fake_message_id",
                "subject": "fake_subject"
            })
        )

        self.assertIsNone(self.message.subject)
        message_updated = self.message.get()

        self.assertTrue(message_updated)
        self.assertEqual("fake_subject", self.message.subject)

    @httpretty.activate
    def test_post_sends_params_and_returns_True(self):
        httpretty.register_uri(
            httpretty.POST, self.uri, status=200,
            body=json.dumps({
                "success": True
            })
        )

        args = {
            "flag_answered": 0,
            "flag_draft": 0,
            "dst_folder": "foo",
            "dst_source": "bar",
            "move": 0,
            "flag_seen": 0,
            "flag_flagged": 0,
            "flag_deleted": 0
        }

        response = self.message.post(**args)

        request_params = httpretty.last_request().body

        self.assertEqual(
            # need to find a better solution for this see urllib and urlparse docs
            "body=&flag_answered=0&move=0&flag_draft=0&dst_folder=foo&flag_flagged=0&dst_source=bar&flag_deleted=0&flag_seen=0",
            request_params
        )

        # a assertTrue({}) passes so we need to assert that the response is equal
        self.assertEqual(True, response)

    @httpretty.activate
    def test_post_returns_dict_if_return_bool_is_False(self):
        httpretty.register_uri(
            httpretty.POST, self.uri, status=200,
            body=json.dumps({
                "success": True
            })
        )

        response = self.message.post(return_bool=False, dst_folder="foobar")

        self.assertEqual({"success": True}, response)


    @httpretty.activate
    def test_delete_returns_true_if_success(self):
        httpretty.register_uri(
            httpretty.DELETE, self.uri,
            status=200,
            body=json.dumps({
                "success": True
            })
        )

        deleted_message = self.message.delete()

        self.assertTrue(deleted_message)

