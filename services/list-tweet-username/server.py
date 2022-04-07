import os

# from google.cloud import bigquery

from flask import Flask, render_template
import grpc

from clear_tweet_proto_pb2 import ClearListRequest, Tweet
from clear_tweet_proto_pb2_grpc import ClearTweetsStub

app = Flask(__name__)

# def query_stackoverflow():
#     client = bigquery.Client()
#     query_job = client.query(
#         """
#         SELECT *
#         FROM `cadeira-nuvem-2122.bq_cloud_2122.db_users`
#         LIMIT 10"""
#     )

#     results = query_job.result()  # Waits for job to complete.

#     for row in results:
#         print(row)
CLEAR_TWEET_LIST_HOST = os.getenv("CLEAR_TWEET_LIST_HOST", "localhost")
CLEAR_TWEET_LIST_PORT = os.getenv("CLEAR_TWEET_LIST_PORT", "50060")
clear_tweet_list_channel = grpc.insecure_channel(f"{CLEAR_TWEET_LIST_HOST}:{CLEAR_TWEET_LIST_PORT}")
clear_tweet_list_client = ClearTweetsStub(clear_tweet_list_channel)


@app.route("/")
def render_homepage():
    clear_list_request = ClearListRequest(
        tweet_list=[Tweet(id=0, text="Some text!", user="username")]
    )
    clear_list_response = clear_tweet_list_client.ClearTweet(
        clear_list_request
    )

    print(clear_list_response)

    return "<h1>HelloWorld</h1>"

#if __name__ == "__main__":
#    query_stackoverflow()