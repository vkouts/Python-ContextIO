from contextio.lib.errors import ArgumentError
from contextio.lib import helpers
from contextio.lib.resources.user import User

from contextio.lib.api import Api

class Lite(Api):
    def get_users(self, **kwargs):
        all_args = ["email", "status", "status_ok", "limit", "offset"]

        params = helpers.sanitize_params(kwargs, all_args)
        return [User(self, obj) for obj in self._request_uri("users", params=params)]

    def post_user(self, **kwargs):
        req_args = ["email", "server", "username", "use_ssl", "port", "type"]

        if "password" in kwargs or "provider_refresh_token" in kwargs and "provider_consumer_key" in kwargs:
            all_args = ["migrate_account_id", "first_name", "last_name"] + req_args
            params = helpers.sanitize_params(kwargs, all_args, req_args)

            return User(self, self._request_uri("users", method="POST", params=params))
        else:
            raise ArgumentError(
                "You must provide either a 'password' or a 'provider_refresh_token'"
                " and a 'provider_consumer_key'")


    def post_connect_token(self, **kwargs):
        req_args = ["callback_url"]
        all_args = ["email", "first_name", "last_name", "status_callback_url"] + req_args

        params = helpers.sanitize_params(kwargs, all_args, req_args)

        return super(Lite, self).post_connect_token(**params)
