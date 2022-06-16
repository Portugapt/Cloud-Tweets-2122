import unittest
import deepdiff

from flask import Request, Flask

from serverless.functions.list_tweet_location.app import main

testapp = Flask(__name__)


class TestListTweetLocation(unittest.TestCase):
    def test_formalize_request_01(self):
        request = Request.from_values(query_string={})
        actual = main._formalize_request(request)
        expected = {'location': 'Lisbon', 'limit': '1000'}

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))
    
    def test_formalize_request_02(self):
        request = Request.from_values(query_string={'location': 'PT'})
        actual = main._formalize_request(request)
        expected = {'location': 'PT', 'limit': '1000'}

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))

    def test_formalize_request_03(self):
        request = Request.from_values(query_string={'location': 'PT', 'limit': '123'})
        actual = main._formalize_request(request)
        expected = {'location': 'PT', 'limit': '123'}

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))