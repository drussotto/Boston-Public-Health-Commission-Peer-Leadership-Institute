from werkzeug.security import check_password_hash
from flask_login import login_user
from pli_user import PliUser
from flask import current_app
# Returns the user_id for the given user if the login was successful
# Otherwise returns None
def validate_login(email, password):
    for user in current_app.config['db'].users.find({ "email_address" : email }):
        # This checks password against the hash we have store, the stored hash includes
        # information such as salts, what algo was used ... etc.
        # So it is best to delegate to werkseug to check here.
        if check_password_hash(user["password"], password):
            return user["_id"]
    return None


# Performs the "login"
# regisers any state needed to manage logged in users (db perhaps?)
# Returns True if we logged someone in
# False if no one is logged in (due to an error or something)
# NOTE: None is a valid input
def perform_login(uid):
    if uid is not None:
        login_user(PliUser.get_auth(uid))
        return True
    else:
        return False
