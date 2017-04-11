from flask import request, render_template, redirect, url_for, current_app, abort
from bson import ObjectId
import json
from pli import get_db
from create_survey_form import CreateSurveyForm, CreateQuestionForm
from survey_response_form import SubmitResponseForm

#Ultimately, return value should look something like this:
"""
{
    "sid": "survey000003",
    name: "survey 3",
    "questions": [
        {
            "question": "When did you last...",
            "answers": {
                    "Within the past week": 25,
                    "Within the past month": 10
                    ...
            }
        }
        ...
    ]
}
"""

#TODO: Refactor into less of a giant blob
def retrieve_response_data(sid):
    ret_val = {
        "sid": sid,
        "questions": []
    }

    db = get_db()

    survey = db.surveys.find_one({"_id": ObjectId(sid)})
    if survey is None:
        abort(404)
    ret_val["name"] = survey["name"]
    questions = [db.survey_questions.find_one({"_id": ObjectId(str(qid))}) for qid in survey["qids"]]

    #[[0, 1, 2, 3], [2, 1, 0 2]...]
    #[[0, 1], [3, 2]...]
    responses = [r["ans_ids"] for r in db.responses.find({"survey_id": str(survey["_id"])} )]
    ret_val["num_responses"] = len(responses)

    for q_idx, question in enumerate(questions):
        new_q = dict(question=question["question"], answers={})

        for ans_idx, ans in enumerate(question["answers"]):
            chosen_count = 0


            for ans_arr in responses:
                if ans_arr[q_idx] == ans_idx: #if they answered the question with this option
                    chosen_count += 1

            new_q["answers"][ans["answer"]] = chosen_count

        ret_val["questions"].append(new_q)

    return ret_val

def create_survey():
    form = CreateSurveyForm(get_db())
    if request.method == "GET":
        return render_template("surveys/create_survey.html")

    else:
        form.set_name(request)
        form.set_questions(request)

        validated, reason = form.validate()
        if validated:
            store_survey(form, get_db())
            return render_template("surveys/successfully_created.html", form=form)
        else:
            abort(400, reason)

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

def delete_survey(sid):
    try:
        removed_survey = get_db().surveys.remove({"_id": ObjectId(sid)})
        if removed_survey is None:
            abort(400, "Invalid survey id: {sid}".format(sid=sid))
        else:
            get_db().responses.remove({"survey_id": str(sid)})
            return "Success!"
    except Exception as e:
        abort(400, str(e))

def delete_survey_question(qid):
    surveys = get_db().surveys.find()

    for survey in surveys:
        for question in survey["qids"]:
            if qid == question:
                abort(400,
                "This question currently exists on a survey. Delete all surveys that reference this question to delete it")

    try:
        removed = get_db().survey_questions.remove({"_id": ObjectId(qid)})
        if removed is None:
            abort(400, "Invalid question id: {qid}".format(qid=qid))
        else:
            return "Success!"
    except Exception as e:
        abort(400, str(e))


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

def get_survey_questions():
    if request.args.get("ajax") is not None:
        if json.loads(request.args.get("ajax")):
            return json.dumps((CreateSurveyForm.get_survey_questions(get_db())))
        else:
            abort(400, "What are you trying to do?")
    else:
        questions = [(q["_id"], q["question"]) for q in get_db().survey_questions.find()]
        return render_template("/surveys/survey_question_list.html", questions=questions)

def get_survey_question(qid):
    question = get_db().survey_questions.find_one({"_id": ObjectId(qid)})

    if question is None:
        abort(404)
    else:
        return render_template("/surveys/survey_question.html", question=question)



def store_question(form, db):
    return db.survey_questions.insert_one(form.as_mongo_doc())

def store_survey(form, db):
    return db.surveys.insert_one(form.as_mongo_doc())

def store_response(form, db):
    return db.responses.insert_one(form.as_mongo_doc())
