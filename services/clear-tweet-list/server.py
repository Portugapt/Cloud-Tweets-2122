import os

from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from clear_tweet_proto_pb2 import (
    Tweet,
    ClearListRequest,
    ClearListResponse
)
import clear_tweet_proto_pb2_grpc

class ClearTweetsService(clear_tweet_proto_pb2_grpc.ClearTweetsServicer):
    def ClearTweet(self, request, context):
        results = []

        for row in request.tweet_list:
            new_id = row.id
            new_text = row.text
            new_user = row.user

            results.append(Tweet(id = new_id, text = new_text, user = new_user))

        return ClearListResponse(tweet_list=results)

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    clear_tweet_proto_pb2_grpc.add_ClearTweetsServicer_to_server(
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
    CLEAR_TWEET_LIST_PORT = os.getenv("CLEAR_TWEET_LIST_PORT", "50060")
    server.add_insecure_port(f"[::]:{CLEAR_TWEET_LIST_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    print("Service is running...")