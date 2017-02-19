from pymongo import MongoClient
from flask import Flask, render_template, abort, url_for, request, current_app, redirect, flash
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
import mongomock
import pli
import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)
Bootstrap(application)
login_manager = LoginManager()
login_manager.init_app(application)
application.url_map.strict_slashes = False
application.secret_key = "We should make this more secret when we do this 4 real"

application.config["db"] = MongoClient().pli



@login_manager.user_loader
def load_pli_user(uid):
    return pli.PliUser.get(uid)

@application.route('/login', methods = [ "POST", "GET" ])
def login():
    if request.method == "GET":
        form = pli.LoginForm()
        return render_template("login.html", form=form)
    if request.method == "POST":
        form = pli.LoginForm(request.form)
        if form.validate():
            uid = pli.validate_login(*form.as_args())
            if pli.perform_login(uid):
                n = request.args.get("next")
                to = n if n is not None else "index"
                if to == "index":
                    return redirect(url_for(to))
                else:
                    return redirect(url_for('page', path=to+".html"))
                # TODO indicate the failure on the login page ...
        return redirect(url_for('login'))
    return abort(404)

        
@application.route('/')
def index():
    return render_template("index.html")

@application.route('/page/<path:path>')
def page(path):
    try:
      return render_template(path)
    except TemplateNotFound:
        abort(404)

@application.errorhandler(404)
def page_not_found(e):
    return page("404.html"), 404


# override_url_for automatically adds a timestamp query parameter to
# static files (e.g. css) to avoid browser caching issues
@application.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(application.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# Adds a "file_url_for" global in the templates
# allows them to get the url for a templated html page
def file_url_for(name):
    return dated_url_for("page", path=name)
application.add_template_global(file_url_for, "file_url_for")

# run the application.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)
