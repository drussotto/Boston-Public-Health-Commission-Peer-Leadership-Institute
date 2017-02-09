from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound

# EB looks for an 'application' callable by default.
application = Flask(__name__)
Bootstrap(application)

@application.route('/')
def index():
    return render_template("index.html", title = "PLI")

@application.route('/<path:path>/')
def page(path):
    try:
      return render_template(path)
    except TemplateNotFound:
      abort(404)

@application.errorhandler(404)
def page_not_found(e):
    return page("404.html"), 404

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)
