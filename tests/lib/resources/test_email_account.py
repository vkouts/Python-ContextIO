from mock import Mock
import unittest

from contextio.lib.resources.email_account import EmailAccount


class TestEmailAccount(unittest.TestCase):

    def test_constructor_sets_attributes_on_object(self):
        email_address = EmailAccount(Mock(), {"label": "fake_label"})

        self.assertTrue(hasattr(email_address, "status"))
        self.assertTrue(hasattr(email_address, "resource_url"))
        self.assertTrue(hasattr(email_address, "type"))
        self.assertTrue(hasattr(email_address, "authentication_type"))
        self.assertTrue(hasattr(email_address, "use_ssl"))
        self.assertTrue(hasattr(email_address, "server"))
        self.assertTrue(hasattr(email_address, "label"))
        self.assertTrue(hasattr(email_address, "username"))
        self.assertTrue(hasattr(email_address, "port"))
