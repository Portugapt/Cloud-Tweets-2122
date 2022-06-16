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

def query():
    client = bigquery.Client()

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
def main(request):
    
    results = query()

    data = {'tweets': json.dumps(results)}
    url = os.getenv("CLEAR_LIST_FUNCTION_URL", "http://localhost:8081")
    clear_response = requests.post(url, data=data)

    response = app.response_class(
        response=clear_response,
        status=200,
        mimetype='application/json'
    )
    return response