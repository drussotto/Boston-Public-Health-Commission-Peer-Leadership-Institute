from flask import Flask, render_template, abort, url_for, request, current_app
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound
import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)
Bootstrap(application)
import pli
application.url_map.strict_slashes = False


@application.route('/login', methods = [ "POST", "GET" ])
def login_user():
    if request.method == "GET":
        form = pli.LoginForm()
        return render_template("login.html", form=form)
    else:
        pass

@application.route('/')
def index():
    return render_template("index.html", title = "PLI")

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


def file_url_for(name):
    return dated_url_for("page", path=name)
application.add_template_global(file_url_for, "file_url_for")

# run the application.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)
