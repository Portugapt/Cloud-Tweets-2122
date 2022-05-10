import os

import random

from google.cloud import bigquery
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

from flask import Flask, render_template
import grpc

from auth_proto_pb2 import AuthRequest, ResponseType
from auth_proto_pb2_grpc import AuthenticationStub

app = Flask(__name__)

def query_add_tweet(username, tweettext):
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../../../pythonBigQuery_credentials.json")

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

AUTH_HOST = os.getenv("AUTH_HOST", "localhost")
AUTH_PORT = os.getenv("AUTH_PORT", "50000")
auth_channel = grpc.insecure_channel(f"{AUTH_HOST}:{AUTH_PORT}")
auth_client = AuthenticationStub(auth_channel)


@app.route("/add-tweet/<username>/<password>/<tweetusername>/<tweettext>")
def render_homepage(username, password, tweetusername, tweettext):
    auth_request = AuthRequest(
        username=username, password=password
    )
    auth_response = auth_client.Authenticate(
        auth_request
    )

    if auth_response.response == ResponseType.AUTHORIZED:
        query_add_tweet(tweetusername, tweettext)
        return app.response_class(
                    response="Authorized",
                    status=200
                )
    else:
        return app.response_class(
                    response="Unauthorized",
                    status=401
                )