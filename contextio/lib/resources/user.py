from contextio.lib.resources.base_resource import BaseResource
from contextio.lib.resources.connect_token import ConnectToken
from contextio.lib.resources.email_account import EmailAccount
from contextio.lib.resources.webhook import WebHook


class User(BaseResource):
    resource_id = "id"
    keys = [
        "id", "email_accounts", "email_addresses", "created", "first_name", "last_name",
        "resource_url"
    ]

    def __init__(self, parent, definition):
        super(User, self).__init__(parent, "users/{id}", definition)

    def get(self):
        return super(User, self).get()

    def post(self, **kwargs):
        all_args = ['first_name', 'last_name']

        for prop in all_args:
            value = kwargs.get(prop)
            if value:
                setattr(self, prop, value)

        return super(User, self).post(params=kwargs, all_args=all_args)

    def delete(self):
        return super(User, self).delete()

    def get_connect_tokens(self):
        return [ConnectToken(self, obj) for obj in self._request_uri('connect_tokens')]

    def get_email_accounts(self):
        return [EmailAccount(self, obj) for obj in self._request_uri('email_accounts')]

    def get_webhooks(self):
        return [WebHook(self, obj) for obj in self._request_uri('webhooks')]

    def post_webhook(self, **kwargs):
        req_args = ["callback_url", "failure_notif_url"]

        all_args = [
            "callback_url", "failure_notif_url", "filter_to", "filter_from",
            "filter_cc", "filter_subject", "filter_thread",
            "filter_new_important", "filter_file_name", "filter_folder_added",
            "filter_folder_removed", "filter_to_domain", "filter_from_domain",
            "include_body", "body_type"
        ]

        webhook = super(User, self).post(
            uri="webhooks", params=kwargs, return_bool=False, all_args=all_args,
            required_args=req_args
        )

        if bool(webhook['success']) is False:
            return False

        return WebHook(self, webhook)
