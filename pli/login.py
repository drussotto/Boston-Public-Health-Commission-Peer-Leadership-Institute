from flask import current_app
# Returns the user_id for the given user if the login was successful
# Otherwise returns None
def validate_login(email, password):
    return current_app.config['db'].find(
        { "email_address" : { "$eq" : email }, "password" : { "$eq" : password }},
        {"_id":1}).next()["_id"]
