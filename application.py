from pymongo import MongoClient
from flask import Flask, render_template, abort, url_for, request, current_app, redirect, flash, g, _app_ctx_stack
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_principal import Principal, identity_loaded
from itsdangerous import URLSafeSerializer
import mongomock
import pli
import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config.from_envvar('PLI_SETTINGS')

mail = Mail(application)
principals = Principal(application)
Bootstrap(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view="login"

application.url_map.strict_slashes = False

application.config["db"] = MongoClient().pli
application.config["mail"] = mail
application.config["signer"] = URLSafeSerializer(application.config["SECRET_KEY"])
application.config["principals"] = principals

@application.before_request
def init_g():
    g.db = application.config["db"]
    g.mail = application.config["mail"]
    g.signer = application.config["signer"]
    g.principals = application.config["principals"]


@login_manager.user_loader
def load_pli_user(uid):
    return pli.PliUser.get(uid)

# This function gets called when someone's Identity gets initialized
@identity_loaded.connect_via(application)
def on_identity_loaded(sender, identity):
    return pli.on_identity_loaded(sender, identity)

@application.route('/admin-only')
@pli.ADMIN_PERM.require()
def admin_test():
    return "only admins."

@application.route('/hello')
@login_required
def hello():
    return "hello"


@application.route('/add-role', methods = [ "PUT" ])
@pli.ADMIN_PERM.require(http_exception=403)
def add_role():
    return pli.add_role()

@application.route('/rm-role', methods = [ "DELETE" ])
@pli.ADMIN_PERM.require(http_exception=403)
def rm_role():
    return pli.rm_role()


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

@application.route('/peer-leader-resources')
@pli.PEERLEADER_PERM.require(http_exception=403)
def peer_leader_resources():
    return render_template("peer_leader_resources.html")

@application.route('/')
def index():
    return render_template("index.html")

@application.route('/question', methods = ["POST"])
@application.route('/question/<int:qid>', methods = ["POST"])
def question(qid=1):
    return pli.answer_question(qid)

@application.route('/page/<path:path>')
def page(path):
    try:
      return render_template(path)
    except TemplateNotFound:
        abort(404)

@application.errorhandler(404)
def page_not_found(e):
    return page("404.html"), 404

@application.route("/surveys/create", methods =["POST", "GET"])
#@pli.ADMIN_PERM.require(http_exception=403)
def create_survey():
    return pli.create_survey()

@application.route("/surveys/questions/create", methods =["POST", "GET"])
#@pli.ADMIN_PERM.require(http_exception=403)
def create_question():
    return pli.create_question()




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

# This allows the jinja templates to get todays question directly.
application.add_template_global(pli.get_todays_question, "get_todays_question")
application.add_template_global(pli.get_todays_choices, "get_todays_choices")
application.add_template_global(current_user, "current_user")

#utility for dan because it's a pain closing flask server on windows
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@application.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

# run the application.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)
