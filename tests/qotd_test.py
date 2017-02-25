from testlib import *
import unittest
pli.testing = True

class QOTDTestCase(PliQotdTestCase):

    @with_req_ctxt
    def test_correct_answer(self, client):
        res = post_qotd(client, "a")
        assert_correct_page(self, res)

    @with_req_ctxt
    def test_wrong_answer(self, client):
        res = post_qotd(client, "b")
        assert_wrong_page(self, res)

    @with_req_ctxt
    def test_bad_answer_out_of_bounds(self, client):
        res = post_qotd(client, "q")
        assert_wrong_page(self, res)

    @with_req_ctxt
    def test_bad_answer_string_too_long(self, client):
        res = post_qotd(client, "ABCDEFGHIJKLMNOP")
        assert_wrong_page(self, res)

    @with_req_ctxt
    def test_bad_answer_numbers(self, client):
        res = post_qotd(client, 999)
        assert_wrong_page(self, res)

    @with_req_ctxt
    def test_bad_answer_type_boolean(self, client):
        res = post_qotd(client, "True")
        assert_wrong_page(self, res)
