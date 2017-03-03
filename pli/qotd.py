from flask import request, render_template, current_app
from qotd_form import QotdSubmissionForm
import mongomock
import datetime

def question_count():
    s = current_app.config["db"].questions.count()
    print("Count", s)
    return s

def current_question_number():
    return ((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days) % question_count()
def get_todays_question():
    return current_app.config["db"].questions.find_one({"question_number":current_question_number()})

def get_todays_choices():
    return get_todays_question().choices

def get_question(qid):
    return current_app.config["db"].questions.find_one({"question_number": qid})

def answer_question():
    form = QotdSubmissionForm(request.form)
    answering = get_question(form.qid.data)
    if answering["answer"] == form.answer.data:
        return "Correct"
    else:
        return "Incorrect"
