from testlib import *
import unittest


class QOTDTestCase(PliQotdTestCase):

    @with_test_client
    def test_correct_answer(self, client):
        res = post_qotd(client, "a")
        self.assertEqual("Correct", res.data)

    @with_test_client
    def test_wrong_answer(self, client):
        res = post_qotd(client, "b")
        self.assertEqual("Incorrect", res.data)

    @with_test_client
    def test_bad_answer_out_of_bounds(self, client):
        res = post_qotd(client, "q")
        self.assertEqual("Incorrect", res.data)

    @with_test_client
    def test_bad_answer_string_too_long(self, client):
        res = post_qotd(client, "ABCDEFGHIJKLMNOP")
        self.assertEqual("Incorrect", res.data)

    @with_test_client
    def test_bad_answer_numbers(self, client):
        res = post_qotd(client, 999)
        self.assertEqual("Incorrect", res.data)

    @with_test_client
    def test_bad_answer_type_boolean(self, client):
        res = post_qotd(client, "True")
        self.assertEqual("Incorrect", res.data)
