from collections import deque
from pli import get_db, get_obj_id, datetime_today
from flask import g
from datetime import timedelta

def _list_hd():
    x = get_db().qotd_meta.find_one({})
    if x is not None:
        return x['hd']
    return None

def _q_by_id(id):
    if id is None:
        me = get_obj_id()()
        return {"_id": me, "next": me, "prev": me}
    return get_db().questions.find_one({"_id": id})

def _load_deque():
    dq = deque()
    dq.appendleft(_q_by_id(_list_hd()))
    nxt = dq[0]["next"]
    while nxt != dq[0]["_id"]:
        q = _q_by_id(nxt)
        nxt = q["next"]
        dq.append(q)
    return dq


def _dq():
    if not hasattr(g, 'q_deque'):
        g.q_deque = _load_deque()
    return g.q_deque

def _write_deque(d):
    # upsert = update or insert if not there.
    get_db().qotd_meta.update_one({}, {"$set": {"hd": d[0]["_id"]}}, upsert=True)
    for q in d:
        get_db().questions.update_one({"_id": q["_id"]}, {"$set": q})

def save_question_list(exn):
    if hasattr(g, 'q_deque'):
        _write_deque(g.q_deque)

def get_question_by_id(id):
    return get_db().questions.find_one({"_id": id})

def get_question_by_idx(idx):
    dq = _dq()
    dq.rotate(-idx)
    e = dq[0]
    dq.rotate(idx)
    return e

def insert_question(question, idx=-1):
    dq = _dq()
    if abs(idx) > len(dq):
        raise IndexError("Out of deque size")
    dq.rotate(-idx)
    if not hasattr(dq, '_id'):
        question["_id"] = get_obj_id()()
    question["prev"] = dq[-1]["_id"]
    question["next"] = dq[0]["_id"]
    dq[-1]["next"] = question["_id"]
    dq[0]["prev"] = question["_id"]
    dq.appendleft(question)
    dq.rotate((idx-1) if idx < 0 else idx)

def _find_nxt(q, itr):
    missing = (None, None)
    cur = next(itr, None)
    while cur is not None and \
          cur != q:
        cur = next(itr, None)
    # The returned tuple indicates whether the question was found or not.
    # The first entry is the question, so if that is None it wasn't found.
    # The second entry indicates the next. If that is None that means
    # the question requested is at the end of the list, and the successor must be the
    # beginning of the deque.
    return (missing if cur is None else (cur, next(itr, None)))

def _get_aft_match(q, itr, restart_idx):
    dq = _dq()
    found_q, found_nxt = _find_nxt(q, itr)
    if found_q is None:
        return None
    return found_nxt if found_nxt is not None else dq[restart_idx]

# Returns the succesor question to the given one, or None if the given question
# couldn't be found.
def succ(q):
    # If found is not None and the suc is None, found is at the end
    # so the next must be the first element
    return _get_aft_match(q, iter(_dq()), 0)


# Returns the predecessor question to the given one, or None if the given question
# couldn't be found.
def pred(q):
    # If found is not None and the pred is None, found is at the beginning
    # so the next must be the last element
    return _get_aft_match(q, reversed(_dq()), -1)

def current_question_rotation():
    return [x for x in _dq()]

def _date_to_datetime(d):
    return datetime(d.year, d.month, d.day)

def _log_question():
    today = datetime_today()
    yesterday = today - timedelta(days=1)

    # This check has to do with the possibility of delayed running of the
    # transition job.
    # Really all we need is to put the next question in.
    if get_db().qotd_meta.find_one({"qlog.day": yesterday}) is not None:
        # Current question actually belongs to yesterday
        q_time = yesterday
    else:
        # Current question actually belongs to today
        q_time = today
    get_db().qotd_meta.update_one(
        {},
        {
            "qlog": {
                "$push": {
                    "day": q_time,
                    "qid": get_question_by_idx(0)
                }
            }
        })

def _get_question_log(low=0, high=10):
    meta = get_db().qotd_meta.find_one({})
    l = len(meta["qlog"])
    return meta["qlog"][low:min(l, high)]

def next_day():
    _log_question()
    _incr_head()
    _write_deque(_dq())


def get_q_by_day_diff(d_day):
    if d_day < 0:
        id = _get_question_log(d_day, d_day+1)[0][qid]
        return get_question_by_id(id)
    else:
        return get_question_by_index(d_day)
