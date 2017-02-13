from flask import Flask, render_template, abort, url_for
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound
import os

# EB looks for an 'app' callable by default.
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<path:path>/')
def page(path):
    try:
      return render_template(path)
    except TemplateNotFound:
      abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return page("404.html"), 404

# override_url_for automatically adds a timestamp query parameter to
# static files (e.g. css) to avoid browser caching issues
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run(port=8000)
