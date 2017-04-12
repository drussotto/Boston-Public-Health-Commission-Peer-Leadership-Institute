from flask import request, abort, jsonify, session
from question_list import get_question_by_id, insert_question, disable_question_in_list, reorder_question_list, get_question_by_day, answer_question_list
from pli import get_obj_id, get_db
def reorder_questions():
    new_list = request.get_json()["new_list"]
    new_new_list = []
    for x in new_list:
        new_new_list.append(get_obj_id(x))
        
    if None in new_new_list:
        return abort(400)
    
    reorder_question_list(new_new_list)
    return "", 200

def enable_question():
    qid = request.form.get("qid", None)
    idx = request.form.get("idx", None)
    if qid is None or idx is None:
        return abort(400)
    
    q = get_question_by_id(get_obj_id(qid))
    if q is None:
        return abort(400)
    insert_question(q, idx=int(idx))
    return "", 200

def disable_question(qid):
    if qid is None:
        return abort(400)

    success = disable_question_in_list(get_obj_id(qid))
    if success:
        return "", 200
    else:
        return "", 400
    
def add_question():
    d = request.get_json()
    if "question" not in d or \
       "choices" not in d or \
       "answer" not in d:
        return abort(400)
    
    question_text = d["question"]
    choices = d["choices"]
    answer = d["answer"]
    history = {}
    for key in choices:
        history[key] = 0
    response_count = 0
    return str(get_db().questions.insert_one({
        "question": question_text,
        "choices": choices,
        "answer": answer,
        "history": history,
        "response_count": 0,
        "next": None,
        "prev": None
    }).inserted_id)

def get_rel_date_question():
    try:
        # Check that we got it, and that
        # it is a valid number
        day = request.form.get("day", None)
        if day is None:
            return abort(400)
        day = int(day)

    except ValueError:
        return abort(400)
    
    q = get_question_by_day(int(day))
    del q["next"]
    del q["prev"]
    q["_id"] = str(q["_id"])
    return jsonify(q)


def answer_question():
    qid = request.form.get("qid", None)
    session[qid] = True
    answer = request.form.get("answer", None)

    if qid is None or answer is None:
        return abort(400)

    success = answer_question_list(qid, answer)
    if success:
        return "", 200
    else:
        return abort(400)
    

    
