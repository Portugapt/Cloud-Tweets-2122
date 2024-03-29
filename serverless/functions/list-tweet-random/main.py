import os
from unittest import result

from google.cloud import bigquery
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

from flask import Flask, json

import functions_framework

import requests

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../keys/pythonBigQuery_credentials.json")

def query():
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query = """
            SELECT tweetId, username, tweettext
            FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global`
            ORDER BY RAND()
            LIMIT 1"""
    
    query_job = client.query(query) 

    query_results = query_job.result()  # Waits for job to complete.

    results = []

    for row in query_results:
        results.append({'id':row.tweetId, 'text':row.tweettext, 'user':row.username})

    return results

@functions_framework.http
def list_tweet_random(request):
    results = query()

    # data = {'tweets': json.dumps(results)}
    # url = os.getenv("CLEAR_LIST_FUNCTION_URL", "https://europe-west1-cadeira-nuvem-2122.cloudfunctions.net/clear_tweet_list")

    # creds = service_account.IDTokenCredentials.from_service_account_file(
    #    key_path, target_audience=url)

    # logging.info(creds.valid)

    # authed_session = AuthorizedSession(creds)

    # logging.info(authed_session)

    # # make authenticated request and print the response, status_code
    # resp = authed_session.get(url)

    # logging.info(resp.text)

    # clear_response = requests.post(url, data=data)

    data = {'tweets': json.dumps(results)}
    url = os.getenv("CLEAR_LIST_FUNCTION_URL", "http://localhost:8081")
    clear_response = requests.post(url, data=data)

    response = app.response_class(
        response=clear_response,
        status=200,
        mimetype='application/json'
    )
    return response