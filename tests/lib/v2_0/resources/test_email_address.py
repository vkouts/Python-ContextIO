import json
import httpretty
import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.email_address import EmailAddress


class TestEmailAddress(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.email_address = EmailAddress(self.contextio, {
            "email": "fake@email.com",
            "validated": 1234567890,
            "primary": 1
        })

    def test_constructor_sets_attributes_on_object(self):
        self.assertEqual("fake@email.com", self.email_address.email)
        self.assertEqual(1234567890, self.email_address.validated)
        self.assertEqual(1, self.email_address.primary)

    def test_constructor_allows_email_address_in_definition(self):
        email_address = EmailAddress(self.contextio, {
            "email_address": "fake@email.com",
            "validated": 1234567890,
            "primary": 1
        })

        self.assertEqual("fake@email.com", email_address.email)
        self.assertEqual(1234567890, email_address.validated)
        self.assertEqual(1, email_address.primary)

    @httpretty.activate
    def test_get_updates_object_with_data_from_api(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://api.context.io/2.0/email_addresses/fake@email.com/",
            status=200,
            body=json.dumps({
                "email": "new@email.com",
            }))

        email_address_updated = self.email_address.get()

        self.assertTrue(email_address_updated)
        self.assertEqual("new@email.com", self.email_address.email)

    @httpretty.activate
    def test_delete_removes_email_address(self):
        httpretty.register_uri(
            httpretty.DELETE,
            "https://api.context.io/2.0/email_addresses/fake@email.com/",
            status=200,
            body=json.dumps({
                "success": True
            }))

        email_address_deleted = self.email_address.delete()

        self.assertTrue(email_address_deleted)

    @httpretty.activate
    def test_post_updates_email_address(self):
        httpretty.register_uri(
            httpretty.POST,
            "https://api.context.io/2.0/email_addresses/fake@email.com/",
            status=200,
            body=json.dumps({
                "success": True
            }))

        email_address_updated = self.email_address.post(primary=0)

        self.assertTrue(email_address_updated)
        self.assertEqual(self.email_address.primary, 0)
