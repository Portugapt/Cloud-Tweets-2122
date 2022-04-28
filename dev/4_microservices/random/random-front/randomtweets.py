import os
import datetime

from flask import Flask, request
import grpc

from tweetMessages_pb2 import (
    RandomLangRequest,
    RandomTimeIntervalRequest
)
from tweetLangService_pb2_grpc import RandomLangStub
from tweetTimeService_pb2_grpc import RandomTimeStub

app = Flask(__name__)

randomLang_host = os.getenv("RANDOMLANG_HOST", "localhost")
randomLang__channel = grpc.insecure_channel(f"{randomLang_host}:60110")
randomLang_client = RandomLangStub(randomLang__channel)

randomTime_host = os.getenv("RANDOMTIME_HOST", "localhost")
randomTime__channel = grpc.insecure_channel(f"{randomTime_host}:60120")
randomTime_client = RandomTimeStub(randomTime__channel)

def time_to_str(date_date):
    return date_date.strftime("%Y%m%d%H%M%S")

def str_to_time(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

@app.route("/random/lang", methods=['GET'])
def randomLanguage():
    search_language = request.args.get("language", default="en", type=str)
    randomLang_request = RandomLangRequest(
        lang=search_language)
    randomLang_response = randomLang_client.ReturnRandomLang(
        randomLang_request
    )

    #print(datetime.datetime.strptime(randomLang_response.posted_time, "%Y%m%d%H%M%S"))
    return f'Text: {randomLang_response.text}\nPosted on: {randomLang_response.posted_time}'

@app.route("/random/timeinterval", methods=['GET'])
def randomTimeInterval():
    startTime = request.args.get("startTime", default="20220225000000", type=str)
    endTime= request.args.get("endTime", default="20220226000000", type=str)
    
    randomTime_request = RandomTimeIntervalRequest(
        startTime=startTime,
        endTime=endTime)
    
    randomTime_response = randomTime_client.ReturnRandomTime(
        randomTime_request
    )
    return f'Text: {randomTime_response.text}\nPosted on: {randomTime_response.posted_time}'