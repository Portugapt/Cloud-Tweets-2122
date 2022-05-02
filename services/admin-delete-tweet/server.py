import os

from google.cloud import bigquery
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

from flask import Flask, render_template
import grpc

from auth_proto_pb2 import AuthRequest, ResponseType
from auth_proto_pb2_grpc import AuthenticationStub

app = Flask(__name__)

def query_delete_tweet(tweetId):
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../../../pythonBigQuery_credentials.json")

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

AUTH_HOST = os.getenv("AUTH_HOST", "localhost")
AUTH_PORT = os.getenv("AUTH_PORT", "50060")
auth_channel = grpc.insecure_channel(f"{AUTH_HOST}:{AUTH_PORT}")
auth_client = AuthenticationStub(auth_channel)


@app.route("/delete-tweet/<username>/<password>/<tweetId>")
def render_homepage(username, password, tweetId):
    auth_request = AuthRequest(
        username=username, password=password
    )
    auth_response = auth_client.Authenticate(
        auth_request
    )

    if auth_response.response == ResponseType.AUTHORIZED:
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