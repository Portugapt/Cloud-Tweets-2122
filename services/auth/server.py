import os

from concurrent import futures

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

        return AuthResponse(response=ResponseType.SOMETHING)

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