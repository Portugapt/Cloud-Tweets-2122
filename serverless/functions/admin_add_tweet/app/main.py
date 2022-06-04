import logging
import os
import random
from typing import Any, List

import functions_framework
import requests
from flask import Flask, Request, json
from google.cloud import bigquery
from google.oauth2 import service_account


def _create_app():
    print('INFO: functions.admin_add_tweet.app.main._create_app')

    return Flask(__name__)


def _query_add_tweet(request: Request):
    print('INFO: functions.admin_add_tweet.app.main._query_add_tweet')

    username = request.args.get("username")
    tweettext = request.args.get("tweettext")
    tweetId = request.args.get("tweetId")

    if not tweetId:
        tweetId = random.randint(100000, 1000000000000000000)

    key_path = os.getenv("GOOGLE_ACCOUNT_KEY",
                         "../keys/pythonBigQuery_credentials.json")

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials,
                             project=credentials.project_id,)

    query = """
            INSERT INTO `cadeira-nuvem-2122.bq_cloud_2122.db_global`
            (tweetId, username, tweettext)
            VALUES (@tweetId, @username, @tweettext)"""

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("tweetId", "INTEGER", tweetId),
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("tweettext", "STRING", tweettext)
        ]
    )

    query_job = client.query(query, job_config=job_config)

    _ = query_job.result()  # Waits for job to complete.

    return tweetId


def _valid_request(request: Request) -> List[bool]:
    print('INFO: functions.admin_add_tweet.app.main._valid_request')

    username = request.args.get("username")
    password = request.args.get("password")
    tweetusername = request.args.get("tweetusername")
    tweettext = request.args.get("tweettext")

    argument_present = [
        bool(i) for i in [username, password, tweetusername, tweettext]]

    return argument_present


def _request_login(request: Request, AUTH_SERVER: str) -> int:
    print('INFO: functions.admin_add_tweet.app.main._request_login')

    username = request.args.get("username")
    password = request.args.get("password")

    clear_response = requests.post(AUTH_SERVER, data={'username': username,
                                                      'password': password})

    return clear_response.status_code


@functions_framework.http
def main(request: Any):
    print('INFO: functions.admin_add_tweet.app.main.main')

    app = _create_app()

    url = os.getenv("AUTH_FUNCTION_URL", "http://localhost:8081")

    if not all(_valid_request(request)):
        response = app.response_class(
            response="Querystring parameters: username, password, tweetusername and tweettext",
            status=400
        )
    elif _request_login(request, url) == 200:
        tweetId = _query_add_tweet(request)
        response = app.response_class(
            response="Authorized, tweetId created:" + str(tweetId),
            status=200
        )
    else:
        response = app.response_class(
            response="Unauthorized",
            status=401
        )
    return response
