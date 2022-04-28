import os
import datetime

from flask import Flask, request, render_template
import grpc

from tweetMessages_pb2 import (
    SearchStringRequest,
    SearchUserRequest
)

from searchStringService_pb2_grpc import searchStringStub
from searchUserService_pb2_grpc import searchUsernameStub


app = Flask(__name__)

searchString_host = os.getenv("STRING_HOST", "localhost")
searchString__channel = grpc.insecure_channel(f"{searchString_host}:60210")
searchString_client = searchStringStub(searchString__channel)

searchUsername_host = os.getenv("USERNAME_HOST", "localhost")
searchUsername__channel = grpc.insecure_channel(f"{searchUsername_host}:60220")
searchUsername_client = searchUsernameStub(searchUsername__channel)

@app.route("/search/string", methods=['GET'])
def searchTweetsByString():
    search_string = request.args.get("searchString", default="Hello World", type=str)
    limitTweets = request.args.get("limit", default=3, type=int)

    searchString_request = SearchStringRequest( 
        searchString = search_string,
        limitResults = limitTweets
    )

    searchString_response = searchString_client.service_searchString(
        searchString_request
    )
    return render_template(
        "homepage.html",
        foundTweets=searchString_response.listTweet,
        limitResults=limitTweets
    )

@app.route("/search/username", methods=['GET'])
def searchTweetsByUsername():
    search_username = request.args.get("username", default="MaineMary3", type=str)
    limitTweets = request.args.get("limit", default=3, type=int)

    searchUsername_request = SearchUserRequest( 
        searchUsername = search_username,
        limitResults = limitTweets
    )

    searchUsername_response = searchUsername_client.service_searchUser(
        searchUsername_request
    )
    return render_template(
        "homepage.html",
        foundTweets=searchUsername_response.listTweet,
        limitResults=limitTweets
    )