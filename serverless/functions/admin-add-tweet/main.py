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

def query_add_tweet(username, tweettext):
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../keys/pythonBigQuery_credentials.json")

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    tweetId = random.randint(100000, 1000000000000000000)

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

    query_results = query_job.result()  # Waits for job to complete.

    return tweetId

@functions_framework.http
def admin_add_tweet(request):
    username = request.args.get("username")
    password = request.args.get("password")
    tweetusername = request.args.get("tweetusername")
    tweettext = request.args.get("tweettext")

    if not username or not password or not tweetusername or not tweettext:
        return app.response_class(
                    response="Querystring parameters: username, password, tweetusername and tweettext",
                    status=400
                )

    data = {'username': username, 'password': password}
    url = os.getenv("AUTH_FUNCTION_URL", "http://localhost:8081")
    clear_response = requests.post(url, data=data)

    if clear_response.status_code == 200:
        tweetId = query_add_tweet(tweetusername, tweettext)
        return app.response_class(
                    response="Authorized, tweetId created:" + str(tweetId),
                    status=200
                )
    else:
        return app.response_class(
                    response="Unauthorized",
                    status=401
                )