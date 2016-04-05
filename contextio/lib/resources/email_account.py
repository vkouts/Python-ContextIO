from contextio.lib.resources.base_resource import BaseResource

class EmailAccount(BaseResource):
    resource_id = "label"
    keys = [
        "status", "resource_url", "type", "authentication_type", "use_ssl", "server", "label",
        "username", "port"
    ]

    def __init__(self, parent, definition):
        super(EmailAccount, self).__init__(parent, 'email_accounts/{label}', definition)


