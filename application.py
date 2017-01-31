from flask import Flask, render_template

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def index():
    return render_template("index.html", title = "PLI")

@application.route('/<path:path>/')
def page(path):
    return render_template(path)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)
