from flask import request, render_template, redirect, url_for
from register_form import PliRegistrationForm
def register():
    if request.method == "GET":
        form = PliRegistrationForm()
        return render_template("register.html", form=form)
    else:
        form = PliRegistrationForm(request.form)
        if form.validate():
            (uid, confirmed) = user_exists(form.email)
            if uid and confirmed:
                return redirect(url_for('page', "already_registered.html"))
            # the exists and not confirmed case falls through
            # we will send another email.
            if not uid:
                uid = create_user(form.as_mongo_doc())
            send_confirmation_email(form.email, uid)
            return render_template("reg_email_sent.html")
        return redirect(url_for('register'))

# Checks if a user with the given email already exists in the DB
# returns a tuple whose contents indicate whether the user exists and is
# confirmed or not. The first entry in the tuple indicates whether the user
# exists and is their UID if they exist. The second is True iff the first is not 0 and the user is confirmed
def user_exists(email_to_check):
    # TODO
    return (False, False)

# TODO
# Sends a confirmation email to the given email address.
# The email should contain a confirmation link with a signed version
# of their uid, which they can use to validate their email.
def send_confirmation_email(send_to, uid):
    pass

# TODO
# Commits the new user_document to the DB, and returns the
# "_id" field of the given document once done.
def create_user(user_document):
    return 1
