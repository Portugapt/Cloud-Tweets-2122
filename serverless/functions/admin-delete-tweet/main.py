import os
import random

from google.cloud import bigquery
from google.oauth2 import service_account

from flask import Flask, json

import functions_framework

import requests

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

def query_delete_tweet(tweetId):
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../keys/pythonBigQuery_credentials.json")

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query = """
            DELETE FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global`
            WHERE tweetId = @tweetId"""
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("tweetId", "INT64", tweetId),
        ]
    )

    query_job = client.query(query, job_config=job_config) 

    query_results = query_job.result()  # Waits for job to complete.

@functions_framework.http
def admin_delete_tweet(request):
    username = request.args.get("username")
    password = request.args.get("password")
    tweetId = request.args.get("tweetid")

    if not username or not password or not tweetId:
        return app.response_class(
                    response="Querystring parameters: username, password and tweetid",
                    status=400
                )

    data = {'username': username, 'password': password}
    url = os.getenv("AUTH_FUNCTION_URL", "http://localhost:8081")
    clear_response = requests.post(url, data=data)

    if clear_response.status_code == 200:
        query_delete_tweet(tweetId)
        return app.response_class(
                    response="Authorized",
                    status=200
                )
    else:
        return app.response_class(
                    response="Unauthorized",
                    status=401
                )