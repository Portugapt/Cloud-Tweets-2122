from concurrent import futures

import os

from datetime import datetime

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from tweetMessages_pb2 import (
    TimeIntervalRequest
)

import LocationListService_pb2_grpc

BDlocation_host = os.getenv("LOCATIONBD_HOST", "localhost")
BDlocation__channel = grpc.insecure_channel(f"{BDlocation_host}:60312")
BDlocation_client = LocationListService_pb2_grpc.BD_LocationsStub(BDlocation__channel)


class CleanLocationsService(LocationListService_pb2_grpc.ServiceLocationsServicer):
    def LocationsCleaner(self, request, context):

        locations_request = TimeIntervalRequest(
            startTime = request.startTime,
            endTime = request.endTime
        )

        locations_response = BDlocation_client.RetrieveLocations(
            locations_request
        )

        ## TODO : Implement Cleaner with country-list Package

        return locations_response

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    LocationListService_pb2_grpc.add_ServiceLocationsServicer_to_server(
        CleanLocationsService(), server
    )
    
    # server.add_secure_port("[::]:443", creds)
    server.add_insecure_port("[::]:60311")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()