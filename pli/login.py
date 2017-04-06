from flask import Flask, render_template, abort, url_for, request, current_app, redirect, flash, g
from flask_login import login_user, current_user, logout_user
from roles import set_identity, remove_identity
from pli_user import PliUser
from login_form import LoginForm
from flask import current_app
from helpers import redir_query_next
from passwords import check_hash

# Returns the user_id for the given user if the login was successful
# Otherwise returns None
def validate_login(email, password):
    for user in current_app.config['db'].users.find({ "email_address" : email }):
        # This checks password against the hash we have store, the stored hash includes
        # information such as salts, what algo was used ... etc.
        # So it is best to delegate to werkseug to check here.
        if check_hash(user["password"], password):
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
        # Tell Flask-Principal the identity changed
        set_identity(uid)
        return True
    else:
        return False

def logout():
    logout_user()
    # Tell Flask-Principal the user is anonymous
    remove_identity()
    return redirect('/')

def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template("login.html", next=request.args.get("next"))
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            uid = validate_login(*form.as_args())
            if perform_login(uid):
                return redir_query_next()
        # TODO indicate the failure on the login page ...
        return redirect(url_for('login'))
    return abort(404)
