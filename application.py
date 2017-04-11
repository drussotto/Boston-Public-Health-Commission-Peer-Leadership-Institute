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


login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view="login"

# Function to prevent usage of these names directly
# use the get_* functions in pli
def init_services():
    db = MongoClient().pli
    mail = Mail(application)
    principals = Principal(application)
    gridfs_ = gridfs.GridFS(db)
    Bootstrap(application)

    application.url_map.strict_slashes = False

    application.config["db"] = db
    application.config["mail"] = mail
    application.config["signer"] = URLSafeSerializer(application.config["SECRET_KEY"])
    application.config["principals"] = principals
    application.config["gridfs"] = gridfs_

init_services()
with application.app_context():
    # Hook to give any additional setup required.
    pli.pli_init()

@login_manager.user_loader
def load_pli_user(uid):
    return pli.PliUser.get(uid)

# This function gets called when someone's Identity gets initialized
@identity_loaded.connect_via(application)
def on_identity_loaded(sender, identity):
    return pli.on_identity_loaded(sender, identity)


@application.route('/')
def index():
    return render_template("index.html")

# WN CARDS
@application.route('/add-wn-card', methods = [ "POST"])
@login_required
@pli.editor_perm
def add_wn_card():
    return pli.add_wn_card()

@application.route('/manage/slideshow', methods= ["GET"])
@login_required
@pli.editor_perm
def manage_whats_new():
    return pli.manage_whats_new()

@application.route('/set-wn-cards', methods = [ "POST"])
@login_required
@pli.editor_perm
def set_wn_cards():
    return pli.set_wn_cards()
# / WN CARDS

# BLOG
@application.route('/blog', methods = [ "GET" ])
def get_blog_page():
    return pli.get_blog()

@application.route('/blog/show', methods = [ "GET" ])
def show_blog_page():
    return pli.show_blog_page()

@application.route('/blog/add', methods = [ "POST", "GET" ])
@login_required
@pli.editor_perm
def add_user_content():
    return pli.add_blog_page()

@application.route('/blog/remove', methods = [ "POST" ])
def remove_blog_page():
    return pli.remove_blog_page()

@application.route('/blog/edit', methods = [ "GET", "POST" ])
@login_required
def edit_my_page():
    return pli.edit_blog_page()

# @application.route('/uc/manage/mine', methods = [ "GET", "POST" ])
# @login_required
# def view_my_pages():
#     return pli.view_my_pages()

# @application.route('/uc/manage/getpage', methods = [ "GET" ])
# def get_page_json():
#     return pli.get_page_dict()

# @application.route('/uc/manage/pageofpages', methods = [ "GET" ])
# def get_segmented_page_list():
#     return pli.get_segmented_page_list()

# @application.route('/uc/manage/count')
# def blog_page_count():
#     return pli.blog_page_count()
# / BLOG

# STAFF
@application.route('/staff', methods = [ "GET" ])
def staff():
    return render_template("staff.html")

@application.route('/manage/staff', methods = [ "GET" ])
@login_required
@pli.editor_perm
def manage_staff():
    return pli.manage_staff()

@application.route('/manage/staff/add', methods = [ "POST" ])
@login_required
@pli.editor_perm
def add_staff():
    return pli.add_staff()

@application.route('/manage/staff/edit', methods = [ "POST" ])
@login_required
@pli.editor_perm
def edit_staff():
    return pli.edit_staff()

@application.route('/manage/staff/order', methods = [ "POST" ])
@login_required
@pli.editor_perm
def edit_staff_order():
    return pli.edit_staff_order()

@application.route('/manage/staff/info', methods = [ "GET" ])
@login_required
@pli.editor_perm
def get_staff_info():
    return pli.get_staff_info()
# / STAFF

# ABOUT
@application.route('/about', methods = [ "GET" ])
def about():
    return render_template("about.html")
# / ABOUT

# ROLES
@application.route('/edit-role', methods = [ "PUT" ])
@login_required
@pli.admin_perm
def edit_role():
    return pli.edit_role()

@application.route('/change-roles')
@login_required
@pli.admin_perm
def change_roles():
    return render_template("change_roles.html")
# / ROLES

# ACCOUNT
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

@application.route('/init-pass-reset', methods = [ "POST", "GET" ])
def init_reset_password():
    return pli.init_reset_password()

@application.route('/validate')
def validate():
    if "user" not in request.args:
        return render_template("register_validate.html", valid=False)
    else:
        return pli.validate_user(request.args.get('user'))
# / ACCOUNT

# RESOURCES
@application.route('/peer-leader-resources')
@login_required
@pli.peerleader_perm
def peer_leader_resources():
    return render_template("peer_leader_resources.html")
# / RESOURCES

# QOTD
@application.route('/question', methods = ["POST"])
@application.route('/question/<int:qid>', methods=["POST"])
def question(qid=1):
    return pli.answer_question(qid)
# / QOTD

# SURVEYS
@application.route("/surveys/create", methods =["POST", "GET"])
@login_required
@pli.editor_perm
def create_survey():
    return pli.create_survey()

@application.route("/surveys/questions", methods=["GET"])
@login_required
@pli.editor_perm
def get_survey_questions():
    return pli.get_survey_questions()

@application.route("/surveys/questions/create", methods =["POST", "GET"])
@login_required
@pli.editor_perm
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

@application.route('/surveys/<string:sid>/responses', methods=["GET", "POST"])
@login_required
@pli.editor_perm
def show_survey_results(sid):
    return render_template("/surveys/survey_response.html",
                            results=pli.retrieve_response_data(sid))

@application.route('/surveys/<string:sid>', methods=["DELETE"])
@login_required
@pli.editor_perm
def delete_survey(sid):
    return pli.delete_survey(sid)

@application.route('/surveys/questions/<string:qid>', methods=["GET"])
@login_required
@pli.editor_perm
def get_survey_question(qid):
    return pli.get_survey_question(qid)



@application.route('/surveys/questions/<string:qid>', methods=["DELETE"])
@login_required
@pli.editor_perm
def delete_survey_question(qid):
    return pli.delete_survey_question(qid)

# / SURVEYS

@application.route('/page/<path:path>')
def page(path):
    try:
      return render_template(path)
    except TemplateNotFound:
        abort(404)

# ERRORS
@application.errorhandler(404)
def page_not_found(e):
    return page("404.html"), 404

@application.errorhandler(403)
def bad_request(e):
    return page("403.html"), 403

@application.errorhandler(400)
def bad_request(e):
    if request.form:
        return page("400.html"), 400
    else:
        return e.description, 400
# / ERRORS

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
application.add_template_global(pli.get_login_form, "get_login_form")
application.add_template_global(pli.PliUser.get, "get_user_by_uid")

# This allows the jinja templates to get todays whats new cards
application.add_template_global(pli.WhatsNewCard.get_frontpage_cards, "get_wn_cards")

# This allows the jinja templates to get the list of all whats new cards
application.add_template_global(pli.WhatsNewCard.list_wn_cards, "list_all_wn_cards")

# This allows the jinja templates to get todays whats new cards
application.add_template_global(pli.WhatsNewCard.get_frontpage_cards, "get_wn_cards")

# This allows the jinja templates to get the lists of all roles.
application.add_template_global(pli.get_all_roles, "get_all_roles")

# This allows the jinja templates to get the list of all deletable user content pages.
application.add_template_global(pli.get_deletable_pages, "get_deletable_pages")

# This allows the jinja templates to get the list of user content pages the current user owns.
application.add_template_global(pli.get_my_pages, "get_my_pages")

application.add_template_global(pli.blog_page_count, "blog_page_count")
application.add_template_global(pli.list_active_staff, "list_active_staff")
application.add_template_global(pli.list_inactive_staff, "list_inactive_staff")
application.add_template_global(pli.list_all_users, "list_all_users")
application.add_template_global(pli.has_admin,"has_admin")
application.add_template_global(pli.has_editor,"has_editor")
application.add_template_global(pli.has_peerleader,"has_peerleader")
application.add_template_global(pli.has_user,"has_user")



# run the application.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)
