import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.discovery import Discovery


class TestDiscoveryResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.discovery = Discovery(self.contextio, {
            "email": "fake@email.com",
            "found": True,
            "type": "catpants",
            "imap": {"foo": "bar"},
            "documentation": ["some.url"]
        })

    def test_constructor_sets_attributes_on_object(self):
        self.assertEqual("fake@email.com", self.discovery.email)
        self.assertEqual(True, self.discovery.found)
        self.assertEqual("catpants", self.discovery.type)
        self.assertEqual({"foo": "bar"}, self.discovery.imap)
        self.assertEqual(["some.url"], self.discovery.documentation)
