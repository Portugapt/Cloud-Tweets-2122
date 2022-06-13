import unittest
import deepdiff

from flask import Request, Flask

from serverless.functions.admin_delete_tweet.app import main

testapp = Flask(__name__)


class TestAdminDeleteTweet(unittest.TestCase):
    def test_valid_request_01(self):
        request = Request.from_values(query_string={})
        actual = main._valid_request(request)
        expected = [False, False, False]

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))

    def test_valid_request_02(self):
        request = Request.from_values(query_string={'username': 'test'})

        actual = main._valid_request(request)
        expected = [True, False, False]

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))

    def test_valid_request_03(self):

        request = Request.from_values(query_string={'tweetid': '999',
                                                    'password': 'test_password'})

        actual = main._valid_request(request)
        expected = [False, True, True]

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))

    def test_valid_request_04(self):

        request = Request.from_values(query_string={'tweetid': '999',
                                                    'password': 'test_password',
                                                    'username': 'test_user',})

        actual = main._valid_request(request)
        expected = [True, True, True]

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))