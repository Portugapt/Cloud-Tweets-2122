import logging
import os
from typing import Any, Dict, List

import functions_framework
import requests
from flask import Flask, Request, json
from google.cloud import bigquery
from google.oauth2 import service_account

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _create_app():
    print('INFO: functions.list_tweet_location.app.main._create_app')

    return Flask(__name__)


app = _create_app()


def _query_execution(request) -> List[Dict[str, Any]]:
    print('INFO: functions.list_tweet_location.app.main._query_execution')

    query = """
            SELECT tweetId, username, tweettext
            FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global`
            WHERE location LIKE @location
            LIMIT @limit"""

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "location", "STRING", "%" + request['location'] + "%"),
            bigquery.ScalarQueryParameter("limit", "INT64", request['limit']),
        ]
    )

    return _run_query(query, job_config)


def _run_query(query: str, job_config: bigquery.QueryJobConfig) -> List[Dict[str, Any]]:
    print('INFO: functions.list_tweet_location.app.main._run_query')

#    key_path = os.getenv("GOOGLE_ACCOUNT_KEY",
#                         "No Access Key")
#
#    credentials = service_account.Credentials.from_service_account_file(
#        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
#    )

    client = bigquery.Client(credentials=credentials,
                             project=credentials.project_id,)

    query_job = client.query(query, job_config=job_config)

    return _query_to_dictionary(query_job.result())


def _query_to_dictionary(query_result) -> List[Dict[str, Any]]:
    print('INFO: functions.list_tweet_location.app.main._query_to_dictionary')

    results = []

    for row in query_result:
        results.append(
            {'id': row.tweetId, 'text': row.tweettext, 'user': row.username})

    return results


def _formalize_request(request: Request,
                       default_location: str = 'Lisbon',
                       default_limit: str = '1000') -> Dict[str, Any]:
    print('INFO: functions.list_tweet_location.app.main._formalize_request')

    location = request.args.get("location")
    limit = request.args.get("limit")

    argument_present = [
        bool(i) for i in [location, limit]]

    if not argument_present[0]:
        location = default_location

    if not argument_present[1]:
        limit = default_limit

    return {'location': location, 'limit': limit}


def _clean_tweets(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    print('INFO: functions.list_tweet_location.app.main._clean_tweets')

    data = {'tweets': json.dumps(results)}
    url = os.getenv("CLEAR_LIST_FUNCTION_URL", "http://localhost:8081")
    clear_response = requests.post(url, data=data)

    return clear_response


@functions_framework.http
def list_tweet_location(request):

    formalized_request = _formalize_request(request)

    results = _query_execution(formalized_request)

    if len(results) > 0:
        response = app.response_class(
            response=_clean_tweets(results),
            status=200,
            mimetype='application/json'
        )
    elif len(results) == 0:
        response = app.response_class(
            response="No Tweets found for this location",
            status=204
        )
    else:
        response = app.response_class(
            response="An error happened",
            status=404
        )

    return response
