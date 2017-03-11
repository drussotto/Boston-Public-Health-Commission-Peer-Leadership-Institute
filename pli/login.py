from flask import Flask, render_template, abort, url_for, request, current_app, redirect, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from pli_roles import set_identity, remove_identity
from pli_user import PliUser
from login_form import LoginForm
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
        return render_template("login.html", form=form)
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            uid = validate_login(*form.as_args())
            if perform_login(uid):
                n = request.args.get("next")
                to = n if n is not None else "/"
                if to.startswith('/'):
                    return redirect(str(to))
                elif to.endswith(".html"):
                    return redirect(url_for('page', path=str(to)))
                else:
                    return redirect(str(to))
                # TODO indicate the failure on the login page ...
        return redirect(url_for('login'))
    return abort(404)
