from google.cloud import bigquery
import numpy as np
import pandas as pd

def upload_data(event, context):

    TABLE_SCHEMA = [
    {"name": "rowID","type": "INT64"},
    {"name": "userId","type": "INT64"},
    {"name": "username","type": "STRING"},
    {"name": "acctdesc","type": "STRING"},
    {"name": "location","type": "STRING"},
    {"name": "n_following","type": "INT64"},
    {"name": "n_followers","type": "INT64"},
    {"name": "n_totaltweets","type": "INT64"},
    {"name": "usercreatedts","type": "DATETIME"},
    {"name": "tweetId","type": "INT64"},
    {"name": "tweetcreatedts","type": "DATETIME"},
    {"name": "retweetcount","type": "INT64"},
    {"name": "tweettext","type": "STRING"},
    {"name": "hashtags","type": "STRING"},
    {"name": "language","type": "STRING"},
    {"name": "coordinates","type": "STRING"},
    {"name": "favouritecount","type": "INT64"},
    {"name": "extractedts","type": "DATETIME"}
  ]
    #client = bigquery.Client()
    upload_data = pd.read_csv(f"gs://{event['bucket']}/{event['name']}")
    upload_data.rename(columns={'Unnamed: 0':'rowID',
                                'following': 'n_following', 
                                'followers':'n_followers', 
                                'totaltweets':'n_totaltweets',
                                'userid': 'userId',
                                'tweetid': 'tweetId'}, inplace=True)
    upload_data = upload_data.astype({'usercreatedts': np.datetime64, 'tweetcreatedts':np.datetime64, 'extractedts':np.datetime64})
    upload_data.to_gbq('bq_cloud_2122.db_global', project_id = 'cadeira-nuvem-2122', if_exists = 'append', table_schema=TABLE_SCHEMA)

