import unittest
import deepdiff

from flask import Request, Flask

from serverless.functions.auth.app import main

testapp = Flask(__name__)


class TestAuth(unittest.TestCase):
    def test_valid_request_01(self):
        request = Request.from_values(query_string={})
        actual = main._valid_request(request)
        expected = [False, False]

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))

    def test_valid_request_02(self):
        
        request = Request.from_values(query_string={'password': 'test_password'})
        actual = main._valid_request(request)
        expected = [False, True]

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))

    def test_valid_request_03(self):
            
        request = Request.from_values(query_string={'username': 'test_username',
                                                    'password': 'test_password'})
        actual = main._valid_request(request)
        expected = [True, True]

        self.assertEqual(first={}, second=deepdiff.DeepDiff(actual, expected))

    def _total_rows_in_query_01(self):

        actual = main._total_rows_in_query(1)
        expected = 200

        self.assertEqual(actual, expected)
    
    def _total_rows_in_query_02(self):
    
        actual = main._total_rows_in_query(2)
        expected = 200

        self.assertEqual(actual, expected)
    
    def _total_rows_in_query_03(self):
        
        actual = main._total_rows_in_query(0)
        expected = 401

        self.assertEqual(actual, expected)