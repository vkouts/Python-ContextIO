import helpers
import contextio as c

CONSUMER_KEY = "YOUR_CONTEXTIO_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONTEXTIO_CONSUMER_KEY"

api = c.ContextIO(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    api_version="lite",
    debug=True
)

helpers.headerprint("FETCHING USERS (Lite API)")

lite_users = api.get_users()

print lite_users
print "\n"
print "Found {0} users.".format(len(lite_users))
print "\n"
