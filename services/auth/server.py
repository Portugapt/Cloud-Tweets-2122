import os

from concurrent import futures

from google.cloud import bigquery
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from auth_proto_pb2 import (
    ResponseType,
    AuthRequest,
    AuthResponse
)
import auth_proto_pb2_grpc

class AuthenticationService(auth_proto_pb2_grpc.AuthenticationServicer):
    def Authenticate(self, request, context):

        key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../../../pythonBigQuery_credentials.json")

        credentials = service_account.Credentials.from_service_account_file(
            key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

        query = """
                SELECT username
                FROM `cadeira-nuvem-2122.bq_cloud_2122.db_admin_user`
                WHERE username = @username
                AND password = @password"""
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("username", "STRING", request.username),
                bigquery.ScalarQueryParameter("password", "STRING", request.password),
            ]
        )

        query_job = client.query(query, job_config=job_config) 

        query_results = query_job.result()  # Waits for job to complete.

        if query_results.total_rows > 0:
            return AuthResponse(response=ResponseType.AUTHORIZED)
        else:
            return AuthResponse(response=ResponseType.NOT_AUTHORIZED)

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    auth_proto_pb2_grpc.add_AuthenticationServicer_to_server(
        AuthenticationService(), server
    )
    '''
    with open("server.key", "rb") as fp:
        server_key = fp.read()
    with open("server.pem", "rb") as fp:
        server_cert = fp.read()
    with open("ca.pem", "rb") as fp:
        ca_cert = fp.read()

    creds = grpc.ssl_server_credentials(
        [(server_key, server_cert)],
        root_certificates=ca_cert,
        require_client_auth=True,
    )
    '''
    AUTH_PORT = os.getenv("AUTH_PORT", "50060")
    server.add_insecure_port(f"[::]:{AUTH_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    print("Service is running...")