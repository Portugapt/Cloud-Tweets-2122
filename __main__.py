import pulumi
from pulumi_gcp import storage, bigquery

import json

# Create a GCP resource (Storage Bucket)
bucket_lz = storage.Bucket(resource_name='tweets-landing-zone',
                           opts=pulumi.ResourceOptions(protect=True),
                           location='EU',
                           name='tweets-landing-zone')

bucket_dataproc = storage.Bucket(resource_name='tweets-dataproc',
                                 opts=pulumi.ResourceOptions(protect=True),
                                 location='EU',
                                 name='tweets-dataproc')

# Export the DNS name of the bucket
pulumi.export('tweets-landing-zone', bucket_lz.url)
pulumi.export('tweets-dataproc',  bucket_dataproc.url)

dataset_tweets = bigquery.Dataset(resource_name='bq_cloud_2122',
                                  location='europe-west1',
                                  dataset_id='bq_cloud_2122',
                                  labels={'type': 'bq-dataset', 'env': 'default'})

db_admin_user = bigquery.Table(resource_name='db_admin_user',
                               opts=pulumi.ResourceOptions(protect=True),
                               location='europe-west1',
                               dataset_id=dataset_tweets.dataset_id,
                               tabel_id='db_admin_user',
                               friendly_name='db_admin_user',
                               schema=json.load('resources/db_global_schema.json'))
