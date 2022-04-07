import os

# from google.cloud import bigquery

from flask import Flask, render_template
import grpc

from auth_proto_pb2 import AuthRequest, ResponseType
from auth_proto_pb2_grpc import AuthenticationStub

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
AUTH_HOST = os.getenv("AUTH_HOST", "localhost")
AUTH_PORT = os.getenv("AUTH_PORT", "50060")
auth_channel = grpc.insecure_channel(f"{AUTH_HOST}:{AUTH_PORT}")
auth_client = AuthenticationStub(auth_channel)


@app.route("/")
def render_homepage():
    auth_request = AuthRequest(
        username="test_username", password="test_password"
    )
    auth_response = auth_client.Authenticate(
        auth_request
    )

    print("HELLO")
    print(auth_response)

    return "<h1>HelloWorld</h1>"

#if __name__ == "__main__":
#    query_stackoverflow()