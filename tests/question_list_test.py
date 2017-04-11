from testlib import *
import unittest
from pli import get_question_by_idx, save_question_list, insert_question, succ, pred, get_db, current_question_rotation
from flask import current_app
class TestQuestionList(PliEntireDbTestCase):
    @with_app_ctxt
    def test_read_nothing(self):
        q = get_question_by_idx(0)
        for x in range(-10, 10):
            self.assertEqual(q, get_question_by_idx(x))

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

    @with_app_ctxt
    def test_read_and_save_insert1(self):
        q = get_question_by_idx(0)
        with current_app.test_request_context():
            add_q (range(5))
            self.check_list(q)
            self.check_list(q, dc=-1, f=pred, startc=4)
        with current_app.test_request_context():
            self.check_list(q)
            self.check_list(q, dc=-1, f=pred, startc=4)

        self.assertEqual(6, len(current_question_rotation()))

    @with_app_ctxt
    def test_read_and_save_insert2(self):
        q = get_question_by_idx(0)
        with current_app.test_request_context():
            add_q (range(5), 0)
            self.check_list(q, dc=-1, f=succ, startc=4)
        with current_app.test_request_context():
            self.check_list(q, dc=-1, f=succ, startc=4)

        self.assertEqual(6, len(current_question_rotation()))

    @with_app_ctxt
    def test_get_question_by_day_diff(self):


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
    for x in l:
        insert_question({"num": x}, idx)
