import mongomock
import inspect
from pli import validate_login, PliUser
from application import application as pli

# Note that the "real_pass" field for these won't be present in the actual db
# just there for convinience during testing.
user1 = {
    "_id": 12345,
    "email_address": "the.principal@gmail.com",
    "real_pass":"iamsecret",
    "password": 'pbkdf2:sha1:1000$FmjdX5b2$c23a5cefc39cc669f3e193670c3c122041266f26',
    "first_name": "Bob",
    "last_name": "Smith",
    "confirmed": True,
    "organization": {
        "name": "Boston Latin",
        "type": "School",
        "region": "Dorchester"
    }
}

user2 = {
    "_id": 23456,
    "email_address": "iloveindoortennis@gmail.com",
    "real_pass":"youcantseeme",
    "password": "pbkdf2:sha1:1000$HDOj8diN$62524eb1619b6ee167aeb1d6116ad6075a5bf3cb",
    "first_name": "Alice",
    "last_name": "Da Example",
    "confirmed": False,
    "organization": {
        "name": "Squashbusters",
        "type": "Community Organization",
        "region": "Roxbury"
    }
}

user3 = {
    "_id": 34567,
    "email_address": "iamastudent@someschool.org",
    "real_pass": "passw0rd",
    "password": 'pbkdf2:sha1:1000$0nSmVzaw$d02fab4a49fa7db43e50b3345b18522eace34e55',
    "first_name": "Eve",
    "last_name": "Fakename",
    "confirmed": True,
    "organization": None
}

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

users = [user1, user2, user3]
questions = [question1, question2, question3]


def mocked_users():
    db = mongomock.MongoClient().pli
    db.users.insert_many(users)
    return db


def mocked_questions():
    db = mongomock.MongoClient.pli
    db.questions.insert_nmany(questions)
    return db


def check_page(expected_content, *name):
        
    def _check_page(f, d, *msg):
        for s in expected_content:
            f(s in d, *msg)

    def assert_page(tr, r):
        if len(name) == 1:
            _check_page(tr.assertTrue, r.data, str(name[0]))
        else:
            _check_page(tr.assertTrue, r.data)
            
    def assert_not_page(tr, r):
        if len(name) == 1:
            _check_page(tr.assertFalse, r.data, "Not " + str(name[0]))
        else:
            _check_page(tr.assertFalse, r.data)

    return assert_page, assert_not_page

assert_index_page, assert_not_index_page = check_page(["PLI has answers to all your health-related questions","Index-Page","Choose a category or search below."],"index")
assert_login_page, assert_not_login_page = check_page(["Email Address","Login","Password"], "login")
assert_res_page, assert_not_res_page = check_page(["Resources-Page"], "resources")
assert_surv_page, assert_not_surv_page = check_page(["Survey-Page"], "surveys")
assert_mail_sent_page, assert_not_mail_sent_page = check_page(["Reg-Email-Send"], "mail-sent")
assert_reg_page, assert_not_reg_page = check_page(["Reg-Page"], "register-page")
assert_alr_reg_page, assert_not_alr_reg_page = check_page(["Already-Reg"], "alr-reg")
assert_bad_vtok_page, assert_not_bad_vtok_page = check_page(["Failed-Token-Valid"], "bad-token-page")
assert_good_vtok_page, assert_not_good_vtok_page = check_page(["Good-Token-Valid"], "good-valid-tok")


def get_u(uid):
    return PliUser(uid, False)


def post_login(client, user, pas, url="/login"):
    return client.post(url, data=dict(
        email=user, 
        password=pas
    ), follow_redirects=True)


def with_login(username, passwd, to=None):
    def decorator(f):
        def actual_function(s, client):
            n = ("?next="+to) if to is not None else ""
            r = post_login(client, username, passwd, url='/login'+n)
            p_len = len(inspect.getargspec(f).args)
            if p_len == 1:
                f(s)
            elif p_len == 2:
                f(s, client)
            elif p_len == 3:
                f(s, client, r)
            else:
                # TODO
                pass
        return actual_function
    return decorator


def with_req_ctxt(f):
    def run_test(s):
        with pli.test_client() as client:
            f(s, client)
    return run_test


def with_test_client(f):
    def run_test(s):
        f(s, pli.test_client())
    return run_test


def with_app_ctxt(f):
    def run_test(s):
        with pli.app_context():
            f(s)
    return run_test

