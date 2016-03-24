import logging
import six

if six.PY2:
    from urllib import quote
else:
    from urllib.parse import quote

from contextio.lib.v2_0 import helpers


class BaseResource(object):
    """Base class for resource objects."""
    keys = []

    def __init__(self, parent, base_uri, definition):
        if definition == "":
            logging.error('Empty response received for ' + base_uri + "")
            return

        try:
            definition = helpers.uncamelize(definition)
        except:
            logging.error('Invalid response received for ' + base_uri + "")
            return

        for k in self.__class__.keys:
            if k in definition:
                setattr(self, k, definition[k])
            else:
                setattr(self, k, None)

        self.parent = parent
        unidict = {six.text_type(k): six.text_type(v) for k, v in definition.items()}
        self.base_uri = quote(base_uri.format(**unidict))

    def _uri_for(self, *elems):
        """Joins API endpoint elements and returns a string."""
        return '/'.join([self.base_uri] + list(elems))

    def _request_uri(
        self, uri_elems, method="GET", params={}, headers={}, body=''):
        """Gathers up request elements and helps form the request object.

        Required Arguments:
            uri_elems: list - list of strings, joined to form the endpoint.

        Optional Arguments:
            method: string - the method of the request. Possible values are
                'GET', 'POST', 'DELETE', 'PUT'
            params: dict - parameters to pass along
            headers: dict - any specific http headers
            body: string - request body, only used on a few PUT statements
        """
        uri = self._uri_for(uri_elems)
        return self.parent._request_uri(
            uri, method=method, params=params, headers=headers, body=body)
