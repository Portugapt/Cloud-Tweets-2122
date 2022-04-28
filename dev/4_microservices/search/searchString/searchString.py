from concurrent import futures

import os
from datetime import datetime

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from tweetMessages_pb2 import (
    ResponseTweet,
    listTweetsResponse
)

import searchStringService_pb2_grpc

from google.cloud import bigquery

class searchStringService(searchStringService_pb2_grpc.searchStringServicer):
    def service_searchString(self, request, context):
        searchString = '(?i)'+request.searchString
        searchLimit = request.limitResults

        QUERY_1 = """
                SELECT tweetId, userId, tweettext, tweetcreatedts, language
                FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global` 
                WHERE REGEXP_CONTAINS(tweettext, @SEARCHSTRING)
                LIMIT @LIMITSEARCH
                """

        # https://hoffa.medium.com/bigquery-performance-tips-searching-for-text-8x-faster-f9314927b8d2
        job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("SEARCHSTRING", 'STRING', searchString),
                        bigquery.ScalarQueryParameter("LIMITSEARCH", 'INTEGER', searchLimit)]
                )
        
        query_job = client.query(QUERY_1, job_config=job_config)

        results = query_job.result()
        results_list = []
        if results.total_rows < 1:
            raise NotFound("No tweet found with containing this string")
        else:
            for e, row in enumerate(results):
                #print(int(row.tweetcreatedts))
                #print(type(row.tweetcreatedts))
                results_list.append(ResponseTweet(tweet_id = row.tweetId,
                                                user_id = row.userId,
                                                text = row.tweettext,
                                                posted_time = row.tweetcreatedts.strftime("%Y-%m-%d %H:%M:%S"),
                                                language = row.language))
        return listTweetsResponse(listTweet=results_list)

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    searchStringService_pb2_grpc.add_searchStringServicer_to_server(
        searchStringService(), server
    )
    
    # server.add_secure_port("[::]:443", creds)
    server.add_insecure_port("[::]:60210")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    client = bigquery.Client()
    serve()