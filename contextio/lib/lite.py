from contextio.lib import helpers
from contextio.lib.resources.user import User

from contextio.lib.api import Api

class Lite(Api):
    def get_users(self, **kwargs):
        all_args = ["email", "status", "status_ok", "limit", "offset"]

        params = helpers.sanitize_params(kwargs, all_args)
        return [User(self, obj) for obj in self._request_uri("users", params=params)]

    def post_user(self, **kwargs):
        req_args = ["email"]
        all_args = ["email", "migrate_account_id", "first_name", "last_name", "server",
            "username", "use_ssl", "port", "type", "password", "provider_refresh_token",
            "provider_consumer_key"
        ]

        params = helpers.sanitize_params(kwargs, all_args, req_args)

        return User(self, self._request_uri("accounts", method="POST", params=params))

    def post_connect_token(self, **kwargs):
        req_args = ["callback_url"]
        all_args = [
            "callback_url", "email", "first_name", "last_name", "status_callback_url"
        ]

        params = helpers.sanitize_params(kwargs, all_args, req_args)

        return super(Lite, self).post_connect_token(**params)
