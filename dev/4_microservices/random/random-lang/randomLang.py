from concurrent import futures

import os

import random
import datetime

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from tweetMessages_pb2 import (
    RandomResponse
)

from google.cloud import bigquery
#os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "../serviceAccount.json")

import tweetLangService_pb2_grpc


class RandomLangService(tweetLangService_pb2_grpc.RandomLangServicer):
    def ReturnRandomLang(self, request, context):
        LANG = request.lang

        QUERY_1 = """
                SELECT tweetId, userId, tweettext, tweetcreatedts, language
                FROM (SELECT rand() as random,  tweetId, userId, tweetcreatedts, tweettext, language
                    FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global` WHERE language = @LANGUAGE  ORDER BY random)
                LIMIT 1
                """
        job_config = bigquery.QueryJobConfig(
                    query_parameters=[bigquery.ScalarQueryParameter("LANGUAGE", 'STRING', LANG)]
                )
        #QUERY_1 = (f'SELECT tweetId, userId, tweettext, tweetcreatedts, language' 
        #            f' FROM (SELECT rand() as random,  tweetId, userId, tweetcreatedts, tweettext, language' 
        #            f' FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global` WHERE language = "{LANG}" ORDER BY random)'
        #            f' LIMIT 1')
        query_job = client.query(QUERY_1, job_config=job_config)
        
        results = query_job.result()
        results_dict = {}
        if results.total_rows < 1:
            raise NotFound("No tweet found in this language")
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
    tweetLangService_pb2_grpc.add_RandomLangServicer_to_server(
        RandomLangService(), server
    )
    
    # server.add_secure_port("[::]:443", creds)
    server.add_insecure_port("[::]:60110")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    client = bigquery.Client()
    serve()