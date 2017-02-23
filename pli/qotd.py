from flask import request, render_template
import mongomock


question1 = {
    "_id": 1,
    "question": "What is the capital of Massachussetts?",
    "choices": {
        "a": "Boston",
        "b": "Washington"
    },
    "answer": "a"
}

question2 = {
    "_id": 2,
    "question": "What does PLI stand for?",
    "choices": {
        "a": "Please Leave It",
        "b": "Pop Lock I",
        "c": "Peer Leadership Institute"
    },
    "answer": "c"
}

question3 = {
    "_id": 3,
    "question": "What is BPHC?",
    "choices": {
        "a": "Boston Public Health Commission",
    },
    "answer": "a",
}

questions = [question1, question2, question3]


def mocked_questions():
    db = mongomock.MongoClient().pli
    db.questions.insert_many(questions)
    return db


def get_question():
    db = mocked_questions()
    result = db.questions.find_one({"_id": 1})
    return result['question'], result['choices']


def answer_question():
    db = mocked_questions()

    todays_question = db.questions.find_one({"_id": 1})
    user_answer = todays_question['choices'].get(request.form["qotd"], "")

    if request.form["qotd"] == todays_question["answer"]:
        return_page = "correct.html"
    else:
        return_page = "wrong.html"
    return render_template(return_page, user_answer=user_answer)
