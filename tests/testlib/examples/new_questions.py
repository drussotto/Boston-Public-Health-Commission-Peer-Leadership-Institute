from mongomock import ObjectId
from pli import datetime_today
from datetime import timedelta

def day(dd):
    return datetime_today() - timedelta(days=dd)

_nq2_id = ObjectId()
_nq1_id = ObjectId()

nq1 = {
    "_id": _nq1_id,
    "question": "What does PLI stand for?",
    "choices": {
        "a": "Please Leave It",
        "b": "Pop Lock I",
        "c": "Peer Leadership Institute"
    },
    "answer": "c",
    # Only nq we have right now, so it loops onto itself
    "_id": _nq1_id,
    "next": _nq2_id,
    "prev": _nq2_id,
    "history": {
        "a": 5,
        "b": 60,
        "c": 0
    },
    "response_count": 65
}


nq2 = {
    "question": "What is the answer?",
    "choices": {
        "a": "This one",
        "b": "This one",
        "c": "This one"
    },
    "answer": "c",
    "_id": _nq2_id,
    "next": _nq1_id,
    "prev": _nq1_id,
    "history": {
        "a": 0,
        "b": 0,
        "c": 1
    },
    "response_count": 1
}


meta = {
    "hd": _nq1_id,
    "qlog": [
        { "day": day(-1) , "qid": _nq2_id },
        { "day": day(-2), "qid": _nq1_id },
        { "day": day(-3), "qid": _nq2_id }
    ]
}



def add_mocked_nquestions(db):
    db.questions.insert_many([nq1, nq2])
    db.qotd_meta.insert(meta)

ex.add(nq1=nq1,
       nq2=nq2,
       nqotd_meta=meta)
