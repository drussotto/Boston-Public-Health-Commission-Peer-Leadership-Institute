from flask_mail import Message
from pli import get_mail, user_by_email, get_db
from flask import request, abort, current_app, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import passwd_reset_for, decode_passwd_reset
from time import time

DEFAULT_RESET_TIMEOUT = 5
def get_reset_timeout():
    if "reset_timeout" in current_app.config:
        minutes = current_app.config["reset_timeout"]
    else:
        minutes = DEFAULT_RESET_TIMEOUT
    return (minutes * 60) # The timeout is expressed in seconds

# Has the token with the given time been used already (for the given user)?
def reset_time_not_used(uid, date):
    return get_db().reset_times.find_one({"user": uid, "time": date}) is None

def is_time_valid(uid, date):
    diff = time() - date
    return \
        diff <= get_reset_timeout() and \
        reset_time_not_used(uid, date)

# Marks the given time as "used" for the given user inside the database
def use_time_for_user(uid, date):
    get_db().reset_times.insert_one({"user": uid, "time": date})

def update_password_for(uid, new_pass):
    get_db().users.update_one({"_id": uid}, {"$set": {"password": gen_hash(new_pass)}})

def gen_hash(s):
    return generate_password_hash(s, method='pbkdf2:sha256')

def check_hash(to_check, expected):
    return check_password_hash(to_check, expected)

def _get_reset_password():
    tkn = request.args.get('token', None)
    if tkn is None:
        return abort(404)
    else:
        return render_template("reset_password.html", token=tkn)

def _post_reset_password():
    tkn = request.form.get('token', None)
    new_pass = request.form.get('new_pass', None)
    if tkn is None or new_pass is None:
        return abort(400)
    user, time = decode_passwd_reset(tkn)
    if is_time_valid(user, time):
        use_time_for_user(user, time)
        update_password_for(user, new_pass)
        return redirect('/')
    else:
        return abort(400)

def _get_init_reset_password():
    return render_template("init_pass_reset.html")

def _post_init_reset_password():
    email = request.form.get("email", None)
    if email is None:
        return abort(400)
    # TODO validate email ....
    msg = Message("PLI Account Password reset",
                  sender="flask@pli-dev.nlocketz.com",
                  recipients=[email])
    usr = user_by_email(email)
    if usr is None:
        return abort(400)

    rst = passwd_reset_for(usr)
    link = "http://%s/pass-reset?token=%s" % (current_app.config["HOST"], rst)
    msg.html = '''
Please click the link below to reset your password.
<br/>
<a href=%s>Click here!</a>
<br/>
If the link doesn't work go to this url: %s
<br/>
''' % (link, link)
    get_mail().send(msg)
    return "", 200

def init_reset_password():
    if request.method == "GET":
        return _get_init_reset_password()
    else:
        return _post_init_reset_password()

def reset_password():
    if request.method == "GET":
        return _get_reset_password()
    else:
        return _post_reset_password()
