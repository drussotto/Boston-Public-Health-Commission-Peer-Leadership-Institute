from flask import request, render_template, current_app, abort
from qotd_form import QotdSubmissionForm
import datetime
from service_util import get_db

def question_count():
    return get_db().questions.count()

def current_question_number():
    return ((datetime.datetime.now() - datetime.datetime(1970,1,1)).days) % question_count()

def get_todays_question():
    return get_db().questions.find_one( {"question_number" : current_question_number() })

def get_todays_choices():
    return get_todays_question().choices

def get_question(qid):
    return get_db().questions.find_one({"question_number": qid})

def answer_question(qid):
    form = QotdSubmissionForm(request.form)
    answering = get_question(qid)
    if form.validate() and \
       answering is not None:
        if form.answer.data in answering["choices"]:
            answer = answering["choices"][form.answer.data]
        else:
            answer = form.answer.data

        if answering["answer"] == form.answer.data:
            return render_template("correct.html", answer=answer)
        else:
            return render_template("wrong.html", answer=answer)

    return abort(404)
