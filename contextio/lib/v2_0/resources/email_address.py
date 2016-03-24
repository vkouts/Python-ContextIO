from contextio.lib.v2_0 import helpers
from contextio.lib.v2_0.resources.base_resource import BaseResource

class EmailAddress(BaseResource):
    """Class to represent the EmailAddress resource.

    Properties:
        email: string - Email address associated to an account.
        validated: integer - Unix timestamp of email address validation time
        primary: integer - whether or not this address is the primary one
            associated to the account. 1 for yes, 0 for no.
    """
    keys = ['email', 'validated', 'primary']

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: Account object - parent is an Account object.
            definition: a dictionary of parameters. The 'email' parameter is
                required to make method calls.
        """
        # allow devs to use email_address instead of email argument
        if definition.get("email_address") is not None:
            definition['email'] = definition['email_address']

        super(EmailAddress, self).__init__(parent, 'email_addresses/{email}', definition)

    def get(self):
        """GET details for a given email address.

        GET method for the email_addresses resource.

        Documentation:
            http://context.io/docs/2.0/accounts/email_addresses#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        self.__init__(self.parent, self._request_uri(''))
        return True

    def post(self, **params):
        """Modifies a given email address.

        POST method for the email_addresses resource.

        Documentation:
            http://context.io/docs/2.0/accounts/email_addresses#id-post

        Optional Arguments:
            primary: int - Set to 1 to make this email address the primary one
                for the account

        Returns:
            Bool
        """
        all_args = ["primary", ]
        params = helpers.sanitize_params(params, all_args)

        # update EmailAddress object with new values
        if "primary" in params:
            self.primary = params["primary"]

        status = self._request_uri("", method="POST", params=params)
        return bool(status["success"])

    def delete(self):
        """Remove a given email address.

        DELETE method for the email_addresses resource.

        Documentation: http://context.io/docs/2.0/accounts/email_addresses#id-delete

        Arguments:
            None

        Returns:
            Bool
        """
        status = self._request_uri('', method='DELETE')
        return bool(status['success'])
