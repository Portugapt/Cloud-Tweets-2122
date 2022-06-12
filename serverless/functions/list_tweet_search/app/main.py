import logging
import os
from typing import Dict, Any, List

from google.cloud import bigquery
from google.oauth2 import service_account

from flask import Flask, json, Request

import functions_framework

import requests

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _create_app():
    print('INFO: functions.list_tweet_search.app.main._create_app')

    return Flask(__name__)

app = _create_app()

def query(request: Dict[str, str]):
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../keys/pythonBigQuery_credentials.json")

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query = """
            SELECT tweetId, username, tweettext
            FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global`
            WHERE username LIKE @search
            OR tweettext LIKE @search
            LIMIT @limit"""

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("search", "STRING", "%" + request['search'] + "%"),
            bigquery.ScalarQueryParameter("limit", "INT64", request['limit']),
        ]
    )
    
    query_job = client.query(query, job_config=job_config) 

    query_results = query_job.result()  # Waits for job to complete.

    results = []

    for row in query_results:
        results.append({'id':row.tweetId, 'text':row.tweettext, 'user':row.username})

    return results

def _formalize_request(request: Request,
                       default_search: str = 'Zelinsky',
                       default_limit: str = '1000') -> Dict[str, Any]:
    print('INFO: functions.list_tweet_location.app.main._formalize_request')

    search = request.args.get("search")
    limit = request.args.get("limit")

    argument_present = [
        bool(i) for i in [search, limit]]

    if not argument_present[0]:
        search = default_search
    
    if not argument_present[1]:
        limit = default_limit

    return {'search': search, 'limit': limit}


def _clean_tweets(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    print('INFO: functions.list_tweet_location.app.main._clean_tweets')

    data = {'tweets': json.dumps(results)}
    url = os.getenv("CLEAR_LIST_FUNCTION_URL", "http://localhost:8081")
    clear_response = requests.post(url, data=data)

    return clear_response

@functions_framework.http
def main(request):

    formalized_request = _formalize_request(request)

    results = query(formalized_request)

    if len(results) > 0:
        response = app.response_class(
            response=_clean_tweets(results),
            status=200,
            mimetype='application/json'
        )
    elif len(results) == 0:
        response = app.response_class(
            response="No Tweets found for this languague",
            status=204
        )
    else:
        response = app.response_class(
            response="An error happened",
            status=404
        )

    return response