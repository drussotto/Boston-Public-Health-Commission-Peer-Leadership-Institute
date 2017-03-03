from flask import current_app
from testlib import *
import unittest


class QOTDTestCase(PliEntireDbTestCase):

    def setUp(self):
        super(QOTDTestCase, self).setUp()
        
    @with_test_client
    def test_correct_answer(self, client):
        res = post_qotd(client, "a", 0)
        assert_correct_page(self, res)

    @with_test_client
    def test_wrong_answer(self, client):
        res = post_qotd(client, "b", 1)
        assert_incorrect_page(self, res)

    @with_test_client
    def test_bad_answer_out_of_bounds(self, client):
        res = post_qotd(client, "q", 0)
        assert_incorrect_page(self, res)

    @with_test_client
    def test_bad_answer_string_too_long(self, client):
        res = post_qotd(client, "ABCDEFGHIJKLMNOP", 0)
        assert_incorrect_page(self, res)

    @with_test_client
    def test_bad_answer_numbers(self, client):
        res = post_qotd(client, 999, -1)
        assert_404_page(self, res)

    @with_test_client
    def test_bad_answer_type_boolean(self, client):
        res = post_qotd(client, "True", 548975)
        assert_404_page(self, res)
