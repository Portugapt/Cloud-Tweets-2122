import os

from google.cloud import bigquery
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

from flask import Flask, render_template, json
import grpc

from clear_tweet_proto_pb2 import ClearListRequest, Tweet
from clear_tweet_proto_pb2_grpc import ClearTweetsStub

app = Flask(__name__)


def query(username, limit):
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../../../pythonBigQuery_credentials.json")

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query = """
            SELECT tweetId, username, tweettext
            FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global`
            WHERE username = @username
            LIMIT @limit"""
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
        ]
    )

    query_job = client.query(query, job_config=job_config) 

    query_results = query_job.result()  # Waits for job to complete.

    results = []

    for row in query_results:
        results.append(Tweet(id=row.tweetId, text=row.tweettext, user=row.username))

    return results

CLEAR_TWEET_LIST_HOST = os.getenv("CLEAR_TWEET_LIST_HOST", "localhost")
CLEAR_TWEET_LIST_PORT = os.getenv("CLEAR_TWEET_LIST_PORT", "50060")
clear_tweet_list_channel = grpc.insecure_channel(f"{CLEAR_TWEET_LIST_HOST}:{CLEAR_TWEET_LIST_PORT}")
clear_tweet_list_client = ClearTweetsStub(clear_tweet_list_channel)

@app.route("/")
def homepage():
    return app.response_class(status=200)

@app.route("/list-tweet-username/<username>")
@app.route("/list-tweet-username/<username>/<limit>")
def render_homepage(username, limit='1000'):
    results = query(username, limit)

    clear_list_request = ClearListRequest(
        tweet_list=results
    )
    clear_list_response = clear_tweet_list_client.ClearTweet(
        clear_list_request
    )

    response = app.response_class(
        response=MessageToJson(clear_list_response),
        status=200,
        mimetype='application/json'
    )
    return response