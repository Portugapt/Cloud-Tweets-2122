import os
import datetime

from flask import Flask, request, render_template
import grpc

from tweetMessages_pb2 import (
    TimeIntervalRequest
)

import LocationListService_pb2_grpc


app = Flask(__name__)

cleanLocation_host = os.getenv("LOCATIONCLEANER_HOST", "localhost")
cleanLocation__channel = grpc.insecure_channel(f"{cleanLocation_host}:60311")
cleanLocation_client = LocationListService_pb2_grpc.ServiceLocationsStub(cleanLocation__channel)

cleanLocation_host = os.getenv("LOCATIONCLEANER_HOST", "localhost")
cleanLocation__channel = grpc.insecure_channel(f"{cleanLocation_host}:60311")
cleanLocation_client = LocationListService_pb2_grpc.ServiceLocationsStub(cleanLocation__channel)


@app.route("/list/location", methods=['GET'])
def locationsByTimeInterval():
    startTime = request.args.get("startTime", default="20220225000000", type=str)
    endTime = request.args.get("endTime", default="20220226000000", type=str)
    
    locations_request = TimeIntervalRequest(
            startTime = request.startTime,
            endTime = request.endTime
        )

    locations_response = cleanLocation_client.LocationsCleaner(
            locations_request
        )

    return render_template(
        "homepage.html",
        foundLangs=locations_response.listLocationResponse,
    )

@app.route("/list/language", methods=['GET'])
def languagesByTimeInterval():
    startTime = request.args.get("startTime", default="20220225000000", type=str)
    endTime = request.args.get("endTime", default="20220226000000", type=str)
    
    languages_request = TimeIntervalRequest(
            startTime = request.startTime,
            endTime = request.endTime
        )

    languages_response = cleanLocation_client.LocationsCleaner(
            languages_request
        )

    return render_template(
        "homepage2.html",
        foundLangs=languages_request.listLocationResponse,
    )