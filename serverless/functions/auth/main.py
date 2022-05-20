import os

from flask import Flask, json

import functions_framework

from google.cloud import bigquery
from google.oauth2 import service_account

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

def authenticate(username, password):
    key_path = os.getenv("GOOGLE_ACCOUNT_KEY", "../keys/pythonBigQuery_credentials.json")

    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query = """
            SELECT username
            FROM `cadeira-nuvem-2122.bq_cloud_2122.db_admin_user`
            WHERE username = @username
            AND password = @password"""
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("password", "STRING", password),
        ]
    )

    query_job = client.query(query, job_config=job_config) 

    query_results = query_job.result()  # Waits for job to complete.

    if query_results.total_rows > 0:
        return 200
    else:
        return 401

@functions_framework.http
def auth(request):
    username = request.form['username']
    password = request.form['password']

    auth_status = authenticate(username, password)

    response = app.response_class(
        status=auth_status
    )
    return response