from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from proto_pb2 import (
    Tweet,
    ClearListRequest,
    ClearListResponse
)
import proto_pb2_grpc

class ClearTweetsService(proto_pb2_grpc.ClearTweetsServicer):
    def ClearTweet(self, request, context):
        new_id = request.tweet_list[0].id + 1
        new_text = request.tweet_list[0].text + " Some more new text!"
        new_user = request.tweet_list[0].user + "_username"

        return ClearListResponse(tweet_list=[Tweet(id=new_id, text=new_text, user=new_user)])

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    proto_pb2_grpc.add_ClearTweetsServicer_to_server(
        ClearTweetsService(), server
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
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()