from flask import request, render_template, redirect, url_for, current_app, abort
from pli import get_db
from create_survey_form import CreateSurveyForm, CreateQuestionForm
from survey_response_form import SubmitResponseForm

def create_survey():
    if request.method == "GET":
        form = CreateSurveyForm()
        form.populate_survey_questions(current_app.config["db"])
        return render_template("surveys/create_survey.html", form=form)

    else:
        form = CreateSurveyForm(request.form)
        form.populate_survey_questions(current_app.config["db"])
        # short circuits if invalid form                                        ??
        if form.validate() and store_survey(form, current_app.config["db"]) != -1:
                return render_template("surveys/successfully_created.html", form=form)
        else:
            return render_template("surveys/error_page.html", form=form)

def create_question():
    if request.method == "GET":
        form = CreateQuestionForm()
        return render_template("surveys/create_survey_question.html", form=form)

    else:
        form = CreateQuestionForm(request.form)
        # short circuits if invalid form                                        ??
        if form.validate() and store_question(form, current_app.config["db"]) != -1:
                return render_template("surveys/successfully_created.html", form=form)
        else:
            return render_template("surveys/error_page.html", form=form)

def complete_survey(sid):
    db = get_db()
    form = SubmitResponseForm(sid, db)

    if request.method == "GET":
        return render_template("surveys/survey.html", survey=form.survey)

    else:
        form.set_timestamp()
        form.set_ans_ids(request)

        validated, error_msg = form.validate()

        if validated:
            store_response(form, get_db())
            return render_template("surveys/successfully_created.html", form=form)
        else:
            abort(400, error_msg)




def store_question(form, db):
    return db.survey_questions.insert_one(form.as_mongo_doc())

def store_survey(form, db):
    return db.surveys.insert_one(form.as_mongo_doc())

def store_response(form, db):
    return db.responses.insert_one(form.as_mongo_doc())
