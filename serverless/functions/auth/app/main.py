import logging
import os
from typing import List

import functions_framework
from flask import Flask, Request
from google.cloud import bigquery
from google.oauth2 import service_account

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _create_app():
    print('INFO: functions.auth.app.main._create_app')

    return Flask(__name__)


app = _create_app()


def authenticate(request: Request) -> int:

    username = request.args.get("username")
    password = request.args.get("password")

    query = """
            SELECT username
            FROM `tweets-cadeira-2122.bq_cloud_2122.db_admin_user`
            WHERE username = @username
            AND password = @password"""

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("password", "STRING", password),
        ]
    )

    authentication = _run_query(query=query, job_config=job_config)

    return _total_rows_in_query(authentication)


def _run_query(query: str, job_config: bigquery.QueryJobConfig) -> int:

    key_path = os.getenv("GOOGLE_ACCOUNT_KEY",
                         "../keys/pythonBigQuery_credentials.json")

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    BQ = bigquery.Client(credentials=credentials,
                         project=credentials.project_id,)

    query_job = BQ.query(query, job_config=job_config)

    query_results = query_job.result()

    return _total_rows_in_query(query_results.total_rows)


def _total_rows_in_query(rows: int) -> int:
    if rows > 0:
        response = 200
    else:
        response = 401

    return response


def _valid_request(request: Request) -> List[bool]:
    print('INFO: functions.auth.app.main._valid_request')

    username = request.args.get("username")
    password = request.args.get("password")

    argument_present = [
        bool(i) for i in [username, password]]

    return argument_present


@functions_framework.http
def main(request):
    if all(_valid_request(request)):
        auth_status = authenticate(request)

        response = app.response_class(
            status=auth_status
        )
    else:
        response = app.response_class(
            response="An error happened",
            status=404
        )
    return response
