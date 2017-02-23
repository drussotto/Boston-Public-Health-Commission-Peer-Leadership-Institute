from pymongo import MongoClient
from flask import Flask, render_template, abort, url_for, request, current_app, redirect, flash, g
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import mongomock
import pli
import os
import config

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config.from_object('config.Config')
mail = Mail(application)
Bootstrap(application)
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view="login"
application.url_map.strict_slashes = False
application.config["db"] = MongoClient().pli
application.config["mail"] = mail

@login_manager.user_loader
def load_pli_user(uid):
    return pli.PliUser.get(uid)

@application.route('/hello')
@login_required
def hello():
    return "hello"

@application.route('/login', methods = [ "POST", "GET" ])
def login():
    return pli.login()

@application.route('/logout')
def logout():
    return pli.logout()
    
@application.route('/register', methods = ["POST", "GET" ])
def register():
    return pli.register()

@application.route('/validate')
def validate():
    if "user" not in request.args:
        return render_template("bad_validation_token.html")
    else:
        return pli.validate_user(request.args.get('user'))
    
@application.route('/')
def index():
    question, choices = pli.get_question()
    return render_template("index.html", question=question, choices=choices)

@application.route('/question', methods = ["POST"])
def question():
    return pli.answer_question()

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
    # Current hack to allow reloading of files.
    if current_app.debug:
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(application.root_path, endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        elif endpoint == 'page':
            pth = values.get('path', None)
            # This will never be None but whatever
            if pth:
                file_path = os.path.join(application.root_path,"templates", pth)
                values["q"] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# Adds a "file_url_for" global in the templates
# allows them to get the url for a templated html page
def file_url_for(name, **kwargs):
    return dated_url_for("page", path=name, **kwargs)
application.add_template_global(file_url_for, "file_url_for")

# run the application.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)
