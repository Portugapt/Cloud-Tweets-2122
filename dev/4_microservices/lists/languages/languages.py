from concurrent import futures

import os

from datetime import datetime

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from tweetMessages_pb2 import (
    listSpokenLanguageResponse,
    SpokenLanguage
)

import LocationListService_pb2_grpc

from google.cloud import bigquery

def time_str_correct(date_str):
    date_object = datetime.strptime(date_str, "%Y%m%d%H%M%S")
    return date_object.strftime("%Y-%m-%d %H:%M:%S")

class BD_LocationsService(LocationListService_pb2_grpc.BD_LocationsServicer):
    def RetrieveLocations(self, request, context):
        startTime = time_str_correct(request.startTime)
        endTime = time_str_correct(request.endTime)


        QUERY_1 = """
                SELECT language, COUNT(language) as frequency
                FROM `cadeira-nuvem-2122.bq_cloud_2122.db_global` 
                WHERE tweetcreatedts BETWEEN @START_TIME AND @END_TIME
                GROUP BY language
                """
        job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("START_TIME", 'STRING', startTime),
                        bigquery.ScalarQueryParameter("END_TIME", 'STRING', endTime)]
                )
        
        query_job = client.query(QUERY_1, job_config=job_config)

        results = query_job.result()

        results_list = []
        if results.total_rows < 1:
            msg = 'No Tweet found for this interval'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        else:
            for e, row in enumerate(results):
                #print(int(row.tweetcreatedts))
                #print(type(row.tweetcreatedts))
                results_list.append(SpokenLanguage(language = row.language,
                                                frequency = row.frequency))
        return listSpokenLanguageResponse(listSpokenLanguage = results_list)

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    LocationListService_pb2_grpc.add_BD_LocationsServicer_to_server(
        BD_LocationsService(), server
    )
    
    # server.add_secure_port("[::]:443", creds)
    server.add_insecure_port("[::]:60312")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    client = bigquery.Client()
    serve()