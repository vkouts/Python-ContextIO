import contextio as c

CONSUMER_KEY = '0nbvylpw'
CONSUMER_SECRET = 'naMIQtyBEbBBstg9'

context_io = c.ContextIO(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET
)

account = context_io.get_accounts()[0]

account_connect_tokens = account.get_connect_tokens()

print account_connect_tokens
# source = account.get_sources()[0]

# connect_tokens = source.get_connect_tokens()

# print account_connect_tokens

# token = account_connect_tokens[0].token
# print token
# print "CONNECT TOKENS"
# print connect_tokens
# print source.get_connect_token(token).token

# print "ADD CONNECT TOKEN"
# print source.post_connect_token(callback_url="https://www.google.com")

# print "CONNECT TOKENS"
# connect_tokens = source.get_connect_tokens()
# print source.delete_connect_token("3o21h07loi7k0lt2")
