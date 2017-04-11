from mongomock import ObjectId
from pli import datetime_today


def day(dd):
    return datetime_today() - timedelta(days=dd)
_nq1_id = ObjectId()
nq1 = {
    "_id": _nq1_id
    "question": "What does PLI stand for?",
    "choices": {
        "a": "Please Leave It",
        "b": "Pop Lock I",
        "c": "Peer Leadership Institute"
    },
    "answer": "c",
    # Only nq we have right now, so it loops onto itself
    "_id": _nq1_id,
    "next": _nq1_id,
    "prev": _nq1_id
}

meta = {
    "hd": nq1["_id"],
    "qlog": [
        { "day": day(0) , "qid": _nq1_id },
        { "day": day(-1), "qid": _nq1_id },
        { "day": day(-2), "qid": _nq1_id }
    ]
}



def add_mocked_nquestions(db):
    db.questions.insert(nq1)
    db.qotd_meta.insert(meta)

ex.add(nq1=nq1,
       nqotd_meta=meta)
