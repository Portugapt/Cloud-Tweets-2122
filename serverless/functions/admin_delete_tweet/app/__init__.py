import unittest
import deepdiff

from flask import Request, Flask

from serverless.functions.admin_add_tweet.app import main

testapp = Flask(__name__)


class TestAuth(unittest.TestCase):
        def test_valid_request_01(self):
            request = Request.from_values(query_string={})
        actual = main._valid_request(request)
        expected = [False, False]

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))