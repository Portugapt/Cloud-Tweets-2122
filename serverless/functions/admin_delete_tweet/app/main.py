import logging
import os
from typing import Any, List

import functions_framework
import requests
from flask import Flask, Request
from google.cloud import bigquery
from google.oauth2 import service_account

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _create_app():
    print('INFO: functions.admin_delete_tweet.app.main._create_app')

    return Flask(__name__)

app = _create_app()

def _run_query(query: str, job_config: bigquery.QueryJobConfig) -> None:
    print('INFO: functions.admin_delete_tweet.app.main._run_query')
    
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../keys/pythonBigQuery_credentials.json")

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    BQ = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query_job = BQ.query(query, job_config=job_config) 

    _ = query_job.result() # Waits for job to complete.

def _query_job(request: Request) -> None:
    print('INFO: functions.admin_delete_tweet.app.main._query_job')

    tweetID = request.args.get("tweetid")

    query = """
        DELETE FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global`
        WHERE tweetId = @tweetId"""
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("tweetId", "INT64", tweetID),
        ]
    )

    _run_query(query, job_config) 

def _valid_request(request: Request) -> List[bool]:
    print('INFO: functions.admin_delete_tweet.app.main._valid_request')

    username = request.args.get("username")
    password = request.args.get("password")
    tweetid = request.args.get("tweetid")

    argument_present = [
        bool(i) for i in [username, password, tweetid]]

    return argument_present

def _request_authentication(request: Request, AUTH_SERVER: str) -> int:
    print('INFO: functions.admin_delete_tweet.app.main._request_login')

    username = request.args.get("username")
    password = request.args.get("password")

    clear_response = requests.post(AUTH_SERVER, data={'username': username,
                                                      'password': password})

    return clear_response.status_code

@functions_framework.http
def main(request: Any):

    url_auth = os.getenv("AUTH_FUNCTION_URL", "http://localhost:8081")

    auth = _request_authentication(request, url_auth)
    
    if not all(_valid_request(request)):
        response =  app.response_class(
                    response="Querystring parameters: username, password and tweetid",
                    status=400
                )

    if auth == 200:
        _query_job(request)
        response =  app.response_class(
                    response="Authorized",
                    status=200
                )
    elif auth == 401:
        response = app.response_class(
            response="Unauthorized",
            status=401
        )
    else:
        response = app.response_class(
            response="An error happened",
            status=404
        )

    return response
