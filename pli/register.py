from flask import request, render_template, redirect, url_for, current_app
from register_form import PliRegistrationForm
from itsdangerous import BadSignature
from flask_mail import Message

def register():
    if request.method == "GET":
        form = PliRegistrationForm()
        return render_template("register.html", form=form)
    else:
        form = PliRegistrationForm(request.form)
        if form.validate():
            (uid, confirmed) = user_exists(form.email.data)
            if uid and confirmed:
                return redirect(url_for('page', path="already_register.html"))
            # the exists and not confirmed case falls through
            # we will send another email.
            if not uid:
                uid = create_user(form.as_mongo_doc())
            send_confirmation_email(form.email.data, uid)
            return render_template("reg_email_sent.html")
        return redirect(url_for('register'))

# Checks if a user with the given email already exists in the DB
# returns a tuple whose contents indicate whether the user exists and is
# confirmed or not. The first entry in the tuple indicates whether the user
# exists and is their UID if they exist. The second is True iff the user exists and the user is confirmed.
def user_exists(email_to_check):
    found = current_app.config["db"].users.find({ "email_address" : email_to_check }).limit(1)
    if found.count() == 0:
        return False, False
    else:
        u = found.next()
        return (u["_id"], u["confirmed"])

def uid_exists(uid):
    return current_app.config["db"].users.find({"_id":uid}).limit(1).count() == 1
    
# TODO
# Sends a confirmation email to the given email address.
# The email should contain a confirmation link with a signed version
# of their uid, which they can use to validate their email.
def send_confirmation_email(send_to, uid):
    msg = Message("PLI Email Confirmation",
                  sender="flask@pli-dev.nlocketz.com",
                  recipients=[send_to])
    link = "http://%s/validate?user=%s" % (current_app.config["HOST"], encode_uid(uid))
    msg.html = '''
Thanks for registering with the PLI!
Please click the link below to confirm your account.
<br/>
<a href=%s>Click here!</a>
<br/>
If the link doesn't work go to this url: %s
<br/>
    ''' % (link, link)
    current_app.config["mail"].send(msg)


# Commits the new user_document to the DB, and returns the
# "_id" field of the given document once done.
def create_user(user_document):
    # TODO check for re-used email...
    lastID = current_app.config["db"].users.find({}, {"_id":1}).sort("_id",-1).limit(1)
    if lastID.count() == 0:
        # Set to 0 so first ID is 1
        lastID = 0
    else:
        lastID = lastID.next()["_id"]    
    doc = user_document.copy()
    newID = str(int(lastID)+1)
    doc["_id"] = newID
    doc["confirmed"] = False
    current_app.config["db"].users.insert(doc)
    return newID


# "confirms" the user whose validation token is given.
# Bad tokens should return the bad_validation template
# otherwise the user's confirmed inside the mongo DB
def validate_user(user_tok):
    toConfirmId = decode_uid(user_tok)
    if toConfirmId is None or not uid_exists(toConfirmId):
        return render_template("bad_validation_token.html")
    else:
        current_app.config["db"].users.update({"_id":toConfirmId}, {"$set": { "confirmed" : "true" }})
        return render_template("good_validation_token.html")


# returns true if the user with the given uid is "confirmed"
def is_confirmed_uid(uid):
    return current_app.config["db"].users.find({"_id":uid}).limit(1).next()["confirmed"]

# returns the encoded uid (using itsdangerous)
# this token will be used for email validation (should be ascii armored, and URL safe)
def encode_uid(uid):
    return current_app.config["signer"].dumps(uid)

# decodes the given encoded uid, the token should have been encoded
# by encoded_uid, and should be made with itsdangerous
# returns None for an invalid uid
def decode_uid(euid):
    try:
        return current_app.config["signer"].loads(euid)
    except BadSignature:
        # We return None for a bad signature
        return None
