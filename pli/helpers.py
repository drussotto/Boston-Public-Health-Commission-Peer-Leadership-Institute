from flask import request, redirect, url_for
from bson import ObjectId
from service_util import get_signer, get_db
from itsdangerous import BadSignature

# This function is necessary because we need to use the mongomock ObjectId
# when in the tests, and the bson one when not. This setup is done before the
# app runs, and the config is overwritten during testing with the mongomock
# version.
def init_help(app):
    app.config["object_id"] = ObjectId

# Performs the redirect to the "next" field in the query arguments.
def redir_query_next():
    n = request.args.get("next")
    to = n if n is not None else "/"
    if to.startswith('/'):
        return redirect(str(to))
    elif to.endswith(".html"):
        return redirect(url_for('page', path=str(to)))
    else:
        return redirect(str(to))

    
# returns the encoded uid (using itsdangerous)
# this token will be used for email validation (should be ascii armored, and URL safe)
def encode_uid(uid):
    return get_signer().dumps(uid)

# decodes the given encoded uid, the token should have been encoded
# by encoded_uid, and should be made with itsdangerous
# returns None for an invalid uid
def decode_uid(euid):
    try:
        return get_signer().loads(euid)
    except BadSignature:
        # We return None for a bad signature
        return None
    
# Does a user with the given id exist?
def uid_exists(uid):
    return get_db().users.find({"_id":uid}).limit(1).count() == 1
