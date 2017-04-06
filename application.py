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
import gridfs
import pli
import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config.from_envvar('PLI_SETTINGS')

# Don't use these directly.
# See service_util.get_db ... etc. for how to get these...
db = MongoClient().pli
mail = Mail(application)
principals = Principal(application)
gridfs = gridfs.GridFS(db)
Bootstrap(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view="login"

application.url_map.strict_slashes = False

application.config["db"] = db
application.config["mail"] = mail
application.config["signer"] = URLSafeSerializer(application.config["SECRET_KEY"])
application.config["principals"] = principals
application.config["gridfs"] = gridfs

pli.init_help(application)

@login_manager.user_loader
def load_pli_user(uid):
    return pli.PliUser.get(uid)

# This function gets called when someone's Identity gets initialized
@identity_loaded.connect_via(application)
def on_identity_loaded(sender, identity):
    return pli.on_identity_loaded(sender, identity)

@application.route('/add-wn-card', methods = [ "POST", "GET" ])
@login_required
@pli.EDITOR_PERM.require(http_exception=403)
def add_wn_card():
    return pli.add_wn_card()

@application.route('/set-wn-cards', methods = [ "POST", "GET" ])
@login_required
@pli.EDITOR_PERM.require(http_exception=403)
def set_wn_cards():
    return pli.set_wn_cards()

@application.route('/uc/add', methods = [ "POST", "GET" ])
@login_required
@pli.EDITOR_PERM.require(http_exception=403)
def add_user_content():
    return pli.add_blog_page()

@application.route('/uc/show', methods = [ "GET" ])
def show_blog_page():
    return pli.show_blog_page()

@application.route('/uc/remove', methods = [ "GET", "POST" ])
def remove_blog_page():
    return pli.remove_blog_page()

@application.route('/uc/manage/mine', methods = [ "GET", "POST" ])
@login_required
def view_my_pages():
    return pli.view_my_pages()

@application.route('/uc/manage/getpage', methods = [ "GET" ])
def get_page_json():
    return pli.get_page_dict()

@application.route('/uc/manage/pageofpages', methods = [ "GET" ])
def get_segmented_page_list():
    return pli.get_segmented_page_list()


@application.route('/staff/add', methods = [ "POST", "GET" ])
@login_required
@pli.EDITOR_PERM.require(http_exception=403)
def add_staff():
    return pli.add_staff()

@application.route('/staff/edit', methods = [ "POST", "GET" ])
@login_required
@pli.EDITOR_PERM.require(http_exception=403)
def edit_staff():
    return pli.edit_staff()

@application.route('/uc/edit', methods = [ "GET", "POST" ])
@login_required
def edit_my_page():
    return pli.edit_blog_page()

@application.route('/add-role', methods = [ "PUT" ])
@login_required
@pli.ADMIN_PERM.require(http_exception=403)
def add_role():
    return pli.add_role()

@application.route('/rm-role', methods = [ "DELETE" ])
@login_required
@pli.ADMIN_PERM.require(http_exception=403)
def rm_role():
    return pli.rm_role()

@application.route('/login', methods = [ "POST", "GET" ])
def login():
    return pli.login()

@application.route('/logout')
def logout():
    return pli.logout()

@application.route('/register', methods = [ "POST", "GET" ])
def register():
    return pli.register()

@application.route('/pass-reset', methods = [ "POST", "GET" ])
def reset_password():
    return pli.reset_password()

@application.route('/init-pass-reset')
def init_reset_password():
    return pli.init_reset_password()

@application.route('/validate')
def validate():
    if "user" not in request.args:
        return render_template("bad_validation_token.html")
    else:
        return pli.validate_user(request.args.get('user'))

@application.route('/peer-leader-resources')
@login_required
@pli.PEERLEADER_PERM.require(http_exception=403)
def peer_leader_resources():
    return render_template("peer_leader_resources.html")

@application.route('/change-roles')
@login_required
@pli.ADMIN_PERM.require(http_exception=403)
def change_roles():
    return render_template("change_roles.html")

@application.route('/')
def index():
    return render_template("index.html")


@application.route('/uc/manage/count')
def blog_page_count():
    return pli.blog_page_count()

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

@application.errorhandler(400)
def bad_request(e): #to-do: Make more generic
    return e.description, 400
    #return render_template("surveys/error_page.html", error=e.description), 400

@application.route("/surveys/create", methods =["POST", "GET"])
@login_required
@pli.EDITOR_PERM.require(http_exception=403)
def create_survey():
    return pli.create_survey()

@application.route("/surveys/questions/create", methods =["POST", "GET"])
@login_required
@pli.EDITOR_PERM.require(http_exception=403)
def create_question():
    return pli.create_question()

@application.route('/card-img/<string:cid>')
@application.route('/img/<string:cid>')
def get_card_img(cid):
    return pli.CarouselCard.send_picture(cid)

@application.route('/surveys')
def show_surveys():

    surveys = [(s["_id"], s["name"]) for s in pli.get_db().surveys.find()]

    return render_template("surveys/survey_list.html", surveys=surveys)

@application.route('/surveys/<string:sid>', methods=["GET", "POST"])
def complete_survey(sid):
    return pli.complete_survey(sid)



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

# This allows the jinja templates to get todays whats new cards
application.add_template_global(pli.WhatsNewCard.get_frontpage_cards, "get_wn_cards")

# This allows the jinja templates to get the list of all whats new cards
application.add_template_global(pli.WhatsNewCard.list_wn_cards, "list_all_wn_cards")

# This allows the jinja templates to get todays whats new cards
application.add_template_global(pli.WhatsNewCard.get_frontpage_cards, "get_wn_cards")

# This allows the jinja templates to get the lists of all roles.
application.add_template_global(pli.all_roles, "get_all_roles")

# This allows the jinja templates to get the list of all deletable user content pages.
application.add_template_global(pli.get_deletable_pages, "get_deletable_pages")

# This allows the jinja templates to get the list of user content pages the current user owns.
application.add_template_global(pli.get_my_pages, "get_my_pages")

application.add_template_global(pli.blog_page_count, "blog_page_count")
application.add_template_global(pli.list_active_staff, "list_active_staff")
application.add_template_global(pli.list_all_users, "list_all_users")



# run the application.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8001)
