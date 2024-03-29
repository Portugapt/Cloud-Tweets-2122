# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import tweetMessages_pb2 as tweetMessages__pb2


class searchUsernameStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.service_searchUser = channel.unary_unary(
                '/searchUsername/service_searchUser',
                request_serializer=tweetMessages__pb2.SearchUserRequest.SerializeToString,
                response_deserializer=tweetMessages__pb2.listTweetsResponse.FromString,
                )


class searchUsernameServicer(object):
    """Missing associated documentation comment in .proto file."""

    def service_searchUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_searchUsernameServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'service_searchUser': grpc.unary_unary_rpc_method_handler(
                    servicer.service_searchUser,
                    request_deserializer=tweetMessages__pb2.SearchUserRequest.FromString,
                    response_serializer=tweetMessages__pb2.listTweetsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'searchUsername', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class searchUsername(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def service_searchUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/searchUsername/service_searchUser',
            tweetMessages__pb2.SearchUserRequest.SerializeToString,
            tweetMessages__pb2.listTweetsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
