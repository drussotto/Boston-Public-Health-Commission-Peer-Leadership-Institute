from flask import request, render_template
def answer_question():
    if request.form["qotd"] == "c":
        return_page = "correct.html"
    else:
        return_page = "wrong.html"
    return render_template(return_page)
