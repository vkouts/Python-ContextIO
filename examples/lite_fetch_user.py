import helpers
import contextio as c

CONSUMER_KEY = "YOUR_CONTEXTIO_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONTEXTIO_CONSUMER_KEY"
EXISTING_USER_ID = "AN_EXISTING_LITE_API_USER_ID" # see the ContextIO dev console

api = c.ContextIO(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    api_version="lite",
    debug=True
)

user = c.User(api, {"id": EXISTING_USER_ID})

helpers.headerprint("FETCHING USER INFO (Lite API)")

user.get()

helpers.cprint("id", user.id)
helpers.cprint("email_accounts", user.email_accounts)
helpers.cprint("email_addresses", user.email_addresses)
helpers.cprint("created", user.created)
helpers.cprint("first_name", user.first_name)
helpers.cprint("last_name", user.last_name)
helpers.cprint("resource_url", user.resource_url)
print "\n"

