import os
from unittest import result

from google.cloud import bigquery
from google.oauth2 import service_account

from flask import Flask, json

import functions_framework

import requests

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

def query():
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../../../../pythonBigQuery_credentials.json")

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

    response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )
    return response

# @functions_framework.http
# def list_tweet_random(request):
#     results = query()

#     headers = {'tweets': json.dumps(results)}
#     clear_response = requests.get('http://localhost:8081', headers=headers)

#     response = app.response_class(
#         response=clear_response,
#         status=200,
#         mimetype='application/json'
#     )
#     return response