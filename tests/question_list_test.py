from testlib import *
import unittest
from pli import get_question_by_idx, save_question_list, insert_question, succ, pred, get_db, current_question_rotation, get_question_by_day, answer_question_list, disable_question, reorder_question_list, disable_question_in_list, answer_question
from flask import current_app
import json

class TestQuestionList(PliEntireDbTestCase):

    @with_app_ctxt
    def test_current_question_rotation(self):
        qs = current_question_rotation()
        self.assertEqual([ex.nq1, ex.nq2], qs)

    @with_app_ctxt
    def test_hd_right_ele(self):
        self.assertEquals(ex.nq1["_id"], get_question_by_idx(0)["_id"])

    def check_list(self, start, dc=1, f=succ, startc=0):
            cur = f(start)
            c = startc
            while cur["_id"] != start["_id"]:
                self.assertEqual(c, cur["num"])
                c+=dc
                cur = f(cur)

    def assertSucc(self, q, expect):
        self.assertEqual(expect, succ(q))

    def assertPred(self, q, expect):
        self.assertEqual(expect, pred(q))
        

    def assertNumKey(self, idx, expect):
        self.assertEqual(expect, get_question_by_idx(idx)["num"])

    def assertIdKey(self, idx, expect):
        self.assertEqual(expect, get_question_by_idx(idx)["_id"])

    @with_app_ctxt
    def test_succ1(self):
        self.assertSucc(ex.nq1, ex.nq2)
        self.assertSucc(ex.nq2, ex.nq1)

    @with_app_ctxt
    def test_pred1(self):
        self.assertPred(ex.nq1, ex.nq2)
        self.assertPred(ex.nq2, ex.nq1)

    @with_app_ctxt
    def test_answer1(self):
        self.assertTrue(answer_question_list(ex.nq1["_id"], "c"))
        q = get_db().questions.find_one({"_id": ex.nq1["_id"]})
        self.assertEqual(ex.nq1["history"]["c"]+1, q["history"]["c"])
        self.assertEqual(ex.nq1["response_count"]+1, q["response_count"])
        q = get_db().questions.find_one({"_id": ex.nq2["_id"]})
        self.assertEqual(ex.nq2["history"]["c"], q["history"]["c"])
        self.assertEqual(ex.nq2["response_count"], q["response_count"])


    @with_app_ctxt
    def test_answer2(self):
        self.assertFalse(answer_question_list(ex.nq1["_id"], "d"))
        q = get_db().questions.find_one({"_id": ex.nq1["_id"]})
        self.assertEqual(ex.nq1["history"]["c"], q["history"]["c"])
        self.assertEqual(ex.nq1["response_count"], q["response_count"])
        q = get_db().questions.find_one({"_id": ex.nq2["_id"]})
        self.assertEqual(ex.nq2["history"]["c"], q["history"]["c"])
        self.assertEqual(ex.nq2["response_count"], q["response_count"])


    @with_app_ctxt
    def test_answer3(self):
        self.assertFalse(answer_question_list(ObjectId(), "d"))
        q = get_db().questions.find_one({"_id": ex.nq1["_id"]})
        self.assertEqual(ex.nq1["history"]["c"], q["history"]["c"])
        self.assertEqual(ex.nq1["response_count"], q["response_count"])
        q = get_db().questions.find_one({"_id": ex.nq2["_id"]})
        self.assertEqual(ex.nq2["history"]["c"], q["history"]["c"])
        self.assertEqual(ex.nq2["response_count"], q["response_count"])

    @with_app_ctxt
    def test_disable1(self):
        insert_question({})
        self.assertTrue(disable_question_in_list(ex.nq1["_id"]))
        self.assertEqual(ex.nq2["_id"], get_question_by_idx(0)["_id"])
        self.assertTrue("question" not in get_question_by_idx(1))

    @with_app_ctxt
    def test_disable2(self):
        insert_question({})
        self.assertTrue(disable_question_in_list(ex.nq2["_id"]))
        self.assertEqual(ex.nq1["_id"], get_question_by_idx(0)["_id"])
        self.assertTrue("question" not in get_question_by_idx(1))

    @with_app_ctxt
    def test_disable3(self):
        self.assertFalse(disable_question_in_list(ObjectId()))
        self.assertEqual(ex.nq1["_id"], get_question_by_idx(0)["_id"])
        self.assertEqual(ex.nq2["_id"], get_question_by_idx(1)["_id"])
        

    @with_app_ctxt
    def test_stupid_rotate(self):
        insert_question({"num": 0}, -2)
        self.assertNumKey(1, 0)
        self.assertIdKey(0, ex.nq1["_id"])
        self.assertIdKey(2, ex.nq2["_id"])

    @with_app_ctxt
    def test_stupid_rotate(self):
        insert_question({"num": 0}, 2)
        self.assertIdKey(0, ex.nq1["_id"])
        self.assertIdKey(1, ex.nq2["_id"])
        self.assertNumKey(2, 0)

    @with_app_ctxt
    def test_reorder(self):
        with current_app.test_request_context():
            reorder_question_list([ex.nq2["_id"], ex.nq1["_id"]])
            self.assertEqual(ex.nq2["_id"], get_question_by_idx(0)["_id"])
            self.assertEqual(ex.nq1["_id"], get_question_by_idx(1)["_id"])
        
        with current_app.test_request_context():    
            self.assertEqual(ex.nq2["_id"], get_question_by_idx(0)["_id"])
            self.assertEqual(ex.nq1["_id"], get_question_by_idx(1)["_id"])

    @with_login(user1)
    def test_reorder_endpoint(self, client):
        res = client.post('/questions/reorder', data=json.dumps({
            "new_list": [str(ex.nq2["_id"]), str(ex.nq1["_id"])]
        }),
        content_type='application/json')
        self.assertEqual(200, res.status_code)
        self.assertEqual(ex.nq2["_id"], get_question_by_idx(0)["_id"])
        self.assertEqual(ex.nq1["_id"], get_question_by_idx(1)["_id"])

        
        
    @with_login(user1)
    def test_enable_question_endpoint(self, client):
        new_id = get_db().questions.insert_one({"stuff": True}).inserted_id
        res = client.post('/questions/enable', data={
            "qid": str(new_id),
            "idx": 0
        })
        self.assertEqual(200, res.status_code)
        self.assertEqual(new_id, get_question_by_idx(0)["_id"])

    @with_login(user1)
    def test_disble_question_endpoint(self, client):
        res = client.post('/questions/disable/'+str(ex.nq1["_id"]))
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(current_question_rotation()))

    @with_login(user1)
    def test_add_question_endpoint(self, client):
        data = json.dumps({
            "question": "What is the answer?",
            "choices": {
                "a": "This one",
                "b": "This one",
                "c": "This one"
            },
            "answer": "c"
        })

        res = client.post('/questions/add',
                          data=data,
                          content_type='application/json')
        
        self.assertEqual(200, res.status_code)
        x = get_db().questions.find_one({"question": "What is the answer?"})
        self.assertTrue("history" in x)

    @with_login(user1)
    def test_add_question_endpoint(self, client):
        data = json.dumps({
            "question": "What is the answer?",
        })

        res = client.post('/questions/add',
                          data=data,
                          content_type='application/json')
        self.assertEqual(400, res.status_code)

    @with_login(user1)
    def test_add_question_endpoint2(self, client):
        data = json.dumps({
            "choices": "What is the answer?",
        })

        res = client.post('/questions/add',
                          data=data,
                          content_type='application/json')
        self.assertEqual(400, res.status_code)

    @with_login(user1)
    def test_add_question_endpoint3(self, client):
        data = json.dumps({
            "answer": "What is the answer?",
        })

        res = client.post('/questions/add',
                          data=data,
                          content_type='application/json')
        self.assertEqual(400, res.status_code)


    @with_login(user1)
    def test_get_rel_date_question_endpoint(self, client):
        def test(x):
            res = client.get('/questions/get_by_day', data={"day": x})
            self.assertEqual(200, res.status_code)
            self.assertEqual(json.loads(res.data)["_id"],
                             str(get_question_by_day(x)["_id"]))
            
        test(-1)
        test(0)
        test(1)

    @with_login(user1)
    def test_answer_question_endpoint(self, client):
        res = client.get('/questions/answer', data=
                         {
                             "qid": ex.nq1["_id"],
                             "answer": "c"
                         })
        self.assertEqual(200, res.status_code)
        q = get_db().questions.find_one({"_id": ex.nq1["_id"]})
        self.assertEqual(ex.nq1["history"]["c"]+1, q["history"]["c"])
        self.assertEqual(ex.nq1["response_count"]+1, q["response_count"])
        q = get_db().questions.find_one({"_id": ex.nq2["_id"]})
        self.assertEqual(ex.nq2["history"]["c"], q["history"]["c"])
        self.assertEqual(ex.nq2["response_count"], q["response_count"])
        
        

    @with_app_ctxt
    def test_read_and_save_insert1(self):
        add_q (range(2))
        def check_order():
            with current_app.test_request_context():
                self.assertIdKey(0, ex.nq1["_id"])
                self.assertIdKey(1, ex.nq2["_id"])
                self.assertNumKey(2, 0)
                self.assertNumKey(3, 1)

        # Yes, this is supposed to be repeated
        # We are testing reload and save on context pop
        check_order()
        check_order()
        self.assertEqual(4, len(current_question_rotation()))

    @with_app_ctxt
    def test_read_and_save_insert2(self):
        add_q (range(2), idx=0)
        def check_order():
            with current_app.test_request_context():
                self.assertNumKey(0, 1)
                self.assertNumKey(1, 0)
                self.assertIdKey(2, ex.nq1["_id"])
                self.assertIdKey(3, ex.nq2["_id"])
        # Yes, this is supposed to be repeated
        # We are testing reload and save on context pop
        check_order()
        check_order()
        self.assertEqual(4, len(current_question_rotation()))

    @with_app_ctxt
    def test_get_question_by_day_diff(self):
        self.assertEqual(ex.nq1["_id"], get_question_by_day(-1)["_id"])

    @with_app_ctxt
    def test_get_question_by_day_diff2(self):
        self.assertEqual(ex.nq1["_id"], get_question_by_day(0)["_id"])

    @with_app_ctxt
    def test_get_question_by_day_diff3(self):
        self.assertEqual(ex.nq2["_id"], get_question_by_day(1)["_id"])

    @with_app_ctxt
    def test_get_question_by_day_diff4(self):
        self.assertEqual(ex.nq1["_id"], get_question_by_day(8)["_id"])

    @with_app_ctxt
    def test_get_question_too_far_back(self):
        self.assertIsNone(get_question_by_day(-8))

    @with_app_ctxt
    def test_insert_random(self):
        insert_question({"new": True}, idx=1)
        self.assertTrue(get_question_by_idx(1)["new"])

    @with_app_ctxt
    def test_insert_gap_error_pos(self):
        with self.assertRaises(IndexError):
            insert_question({"new": True}, idx=5)

    @with_app_ctxt
    def test_insert_gap_error_neg(self):
        with self.assertRaises(IndexError):
            insert_question({"new": True}, idx=-3)


def add_q(l, idx=-1):
    out = []
    for x in l:
        insert_question({"num": x}, idx)
    return out
