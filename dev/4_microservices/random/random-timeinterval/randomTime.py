from concurrent import futures

import os

from datetime import datetime

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from tweetMessages_pb2 import (
    RandomResponse
)

import tweetTimeService_pb2_grpc

from google.cloud import bigquery

def time_str_correct(date_str):
    date_object = datetime.strptime(date_str, "%Y%m%d%H%M%S")
    return date_object.strftime("%Y-%m-%d %H:%M:%S")

class RandomTimeService(tweetTimeService_pb2_grpc.RandomTimeServicer):
    def ReturnRandomTime(self, request, context):
        startTime = time_str_correct(request.startTime)
        endTime = time_str_correct(request.endTime)


        QUERY_1 = """
                SELECT tweetId, userId, tweettext, tweetcreatedts, language
                FROM (SELECT rand() as random,  tweetId, userId, tweetcreatedts, tweettext, language
                    FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global` 
                    WHERE tweetcreatedts BETWEEN @START_TIME AND @END_TIME ORDER BY random)
                LIMIT 1
                """
        job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("START_TIME", 'STRING', startTime),
                        bigquery.ScalarQueryParameter("END_TIME", 'STRING', endTime)]
                )
        
        query_job = client.query(QUERY_1, job_config=job_config)

        results = query_job.result()
        results_dict = {}
        if results.total_rows < 1:
            raise NotFound("No tweet found in this time interval")
        else:
            for e, row in enumerate(results):
                #print(int(row.tweetcreatedts))
                #print(type(row.tweetcreatedts))
                results_dict[e] = RandomResponse(tweet_id = row.tweetId,
                                                user_id = row.userId,
                                                text = row.tweettext,
                                                posted_time = row.tweetcreatedts.strftime("%Y-%m-%d %H:%M:%S"),
                                                language = row.language)
        return results_dict[0]

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    tweetTimeService_pb2_grpc.add_RandomTimeServicer_to_server(
        RandomTimeService(), server
    )
    
    # server.add_secure_port("[::]:443", creds)
    server.add_insecure_port("[::]:60120")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    client = bigquery.Client()
    serve()