import pulumi
from pulumi_gcp import storage, bigquery, apigateway

import base64
from typing import List


# Create a GCP resource (Storage Bucket)
bucket_lz = storage.Bucket(resource_name='tweets-landing-zone',
                           opts=pulumi.ResourceOptions(protect=True),
                           location='EU',
                           name='tweets-landing-zone')

bucket_cloudfunctions = storage.Bucket(resource_name='tweets-cloudfunctions-zip',
                                 opts=pulumi.ResourceOptions(protect=True),
                                 location='EU',
                                 name='tweets-cloudfunctions-zip')

bucket_dataproc = storage.Bucket(resource_name='tweets-dataproc',
                                 opts=pulumi.ResourceOptions(protect=True),
                                 location='EU',
                                 name='tweets-dataproc')

# Export the DNS name of the bucket
pulumi.export('tweets-landing-zone', bucket_lz.url)
pulumi.export('tweets-cloudfunctions-zip', bucket_cloudfunctions.url)
pulumi.export('tweets-dataproc',  bucket_dataproc.url)


# Bigquery

def _load_json_schema(path: str) -> List:
    with open(path, "r") as file:
        return file.read().replace('\n','')

dataset_tweets = bigquery.Dataset(resource_name='bq_cloud_2122',
                                  opts=pulumi.ResourceOptions(
                                      protect=True),
                                  location='europe-west1',
                                  dataset_id='bq_cloud_2122',
                                  labels={'type': 'bq-dataset', 'env': 'default'})

db_admin_user = bigquery.Table(resource_name='db_admin_user',
                               opts=pulumi.ResourceOptions(protect=True),
                               dataset_id=dataset_tweets.dataset_id,
                               table_id='db_admin_user',
                               schema=_load_json_schema('resources/db_admin_user_schema.json'))

db_global = bigquery.Table(resource_name='db_global',
                           opts=pulumi.ResourceOptions(protect=True),
                           dataset_id=dataset_tweets.dataset_id,
                           table_id='db_global',
                           schema=_load_json_schema('resources/db_global_schema.json'))

db_readfiles = bigquery.Table(resource_name='db_readfiles',
                              opts=pulumi.ResourceOptions(protect=True),
                              dataset_id=dataset_tweets.dataset_id,
                              table_id='db_readfiles',
                              schema=_load_json_schema('resources/db_readfiles_schema.json'))

# API

api = apigateway.Api("ukraine-api", api_id="ukraine-api",
    opts=pulumi.ResourceOptions(provider=google_beta))


api_config = apigateway.ApiConfig("ukraine-functions-config",
    api=api.api_id,
    api_config_id="cfg",
    openapi_documents=[apigateway.ApiConfigOpenapiDocumentArgs(
        document=apigateway.ApiConfigOpenapiDocumentDocumentArgs(
            path="serverless/api_gateway/config.yaml",
            contents=(lambda path: base64.b64encode(open(path).read().encode()).decode())("serverless/api_gateway/config.yaml"),
        ),
    )],
    opts=pulumi.ResourceOptions(provider=google_beta))


api_gw_gateway = apigateway.Gateway("ukraine-api-gateway",
    api_config=api_config.id,
    gateway_id="api-gw",
    opts=pulumi.ResourceOptions(provider=google_beta))

