from flask import request, render_template, redirect, url_for, current_app
from register_form import PliRegistrationForm
from flask_mail import Message
from service_util import get_db, get_mail
from helpers import encode_uid, decode_uid, uid_exists
def register():
    if request.method == "GET":
        # Send registration form.
        form = PliRegistrationForm()
        return render_template("register.html", form=form)
    else:
        # Validate registration form.
        form = PliRegistrationForm(request.form)
        if form.validate():
            # Make sure they don't exist, and perform registration.
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
    found = get_db().users.find({ "email_address" : email_to_check }).limit(1)
    if found.count() == 0:
        return False, False
    else:
        u = found.next()
        return (u["_id"], u["confirmed"])


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
    get_mail().send(msg)


# Commits the new user_document to the DB, and returns the
# "_id" field of the given document once done.
def create_user(user_document):
    # TODO check for re-used email...
    lastID = get_db().users.find({}, {"_id":1}).sort("_id",-1).limit(1)
    # Special case for the very first user.
    if lastID.count() == 0:
        # Set to 0 so first ID is 1
        lastID = 0
    else:
        lastID = lastID.next()["_id"]
        
    doc = user_document.copy()
    newID = str(int(lastID)+1)
    doc["_id"] = newID
    doc["confirmed"] = False
    doc["roles"] = ""
    get_db().users.insert(doc)
    return newID


# "confirms" the user whose validation token is given.
# Bad tokens should return the bad_validation template
# otherwise the user's confirmed inside the mongo DB
def validate_user(user_tok):
    toConfirmId = decode_uid(user_tok)
    if toConfirmId is None or not uid_exists(toConfirmId):
        return render_template("bad_validation_token.html")
    else:
        get_db().users.update({"_id":toConfirmId}, {"$set": { "confirmed" : "true" }})
        return render_template("good_validation_token.html")


# returns true if the user with the given uid is "confirmed"
def is_confirmed_uid(uid):
    return get_db().users.find({"_id":uid}).limit(1).next()["confirmed"]
