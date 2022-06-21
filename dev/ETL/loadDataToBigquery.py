#!/usr/bin/env python

import logging
from pyspark.sql import SparkSession
from google.cloud import storage
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, TimestampType, LongType

import pandas as pd


logging.basicConfig(level=logging.INFO)

BUCKET = 'tweets-dataproc'
BUCKET_LINK = 'gs://tweets-dataproc'
TEMP_BUCKET = 'cloud-computing-2122-dataproc-temp'

DB_GLOBAL = 'tweets-cadeira-2122:bq_cloud_2122.db_global'
DB_READFILES = 'tweets-cadeira-2122:bq_cloud_2122.db_readfiles'

GLOBAL_SCHEMA = StructType([ \
    StructField("RowID",IntegerType(),False), \
    StructField("userid",LongType(),False), \
    StructField("username",StringType(),False), \
    StructField("acctdesc",StringType(),True), \
    StructField("location", StringType(), True), \
    StructField("n_following", IntegerType(), True), \
    StructField("n_followers", IntegerType(), True), \
    StructField("n_totaltweets", IntegerType(), True), \
    StructField("usercreatedts", TimestampType(), False), \
    StructField("tweetId", LongType(), False), \
    StructField("tweetcreatedts", TimestampType(), False), \
    StructField("retweetcount", IntegerType(), False), \
    StructField("tweettext", StringType(), True), \
    StructField("hashtags", StringType(), False), \
    StructField("language", StringType(), True), \
    StructField("coordinates", StringType(), True), \
    StructField("favouritecount", IntegerType(), True), \
    StructField("extractedts", TimestampType(), False) \
  ])

READFILE_SCHEMA = StructType([StructField('csvfile', StringType(), False)])

# Read txt file of already processed CSV's

# List all available data files
def list_blobs_with_prefix(bucket_name, prefix):
    # https://cloud.google.com/storage/docs/listing-objects#storage-list-objects-python
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    list_of_csvs = []
    """
    print("Blobs:")
    """
    for blob in blobs:
        list_of_csvs.append(blob.name.split("/")[-1])
        # print(blob.name)
    return list_of_csvs

# Update txt file after data is processed
# https://stackoverflow.com/questions/43682521/writing-data-to-google-cloud-storage-using-python
def write_txt_to_bucket(bucket_name, destination_file_name, files_list):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_file_name) 
    ## Use bucket.get_blob('path/to/existing-blob-name.txt') to write to existing blobs
    with blob.open(mode='w') as f:
        f.write('\n'.join(files_list))


## Spark Job

spark = SparkSession \
  .builder \
  .master('yarn') \
  .appName('spark-ETL-Tweets') \
  .getOrCreate()

spark.conf.set('temporaryGcsBucket', TEMP_BUCKET)

# Get the already read files
READFILES = spark.read.format('bigquery') \
  .option("table", DB_READFILES) \
  .load() \
  .select('csvfile') \
  .collect()

# Put into list the already read files
FILES_ALREADY_READ = [row.csvfile for row in READFILES]
#FILES_ALREADY_READ = read_txt_blob(BUCKET, 'control/read_files.txt')

# Create list of files in the data bucket
DATA_IN_BUCKET = list_blobs_with_prefix(BUCKET, 'data/')

# Create list of files to process
FILES_TO_PROCESS = [f'data/{FILE}' for FILE in DATA_IN_BUCKET if FILE not in FILES_ALREADY_READ]


#   .config('spark.jars', 'gs://hadoop-lib/gcs/gcs-connector-hadoop2-latest.jar,gs://spark-lib/bigquery/spark-bigquery-latest.jar') \


logging.info(FILES_ALREADY_READ)
logging.info(DATA_IN_BUCKET)
logging.info(FILES_TO_PROCESS)


for csv_file in FILES_TO_PROCESS:
    ## DOES NOT WORK
    ##sc = SparkContext.getOrCreate()
    ##rdd_csv = sc.wholeTextFiles(f"{BUCKET_LINK}/{csv_file}")
    ##rdd_csv.collect()
    ## WORKS - BUT DOES IT WORK FOR MULTIPLE FILES READ?
    logging.info(f'START: Read csv_file {csv_file} from bucket')

    csv_data = pd.read_csv(f"{BUCKET_LINK}/{csv_file}", parse_dates=[8,10,17])
    logging.info(f'END: Read csv_file {csv_file} from bucket')


    logging.info(f'START: Convert to Spark dataframe')
    dfSpark = spark.createDataFrame(csv_data,schema=GLOBAL_SCHEMA)
    logging.info(f'END: Convert to Spark dataframe')
    logging.info(f'START: Load Spark dataframe to Bigquery')
    dfSpark.write.mode('append') \
            .format('bigquery') \
            .option('table', DB_GLOBAL) \
            .save()
    logging.info(f'END: Load Spark dataframe to Bigquery')

    #### START: Record processed file ####
    logging.info(f'START: Writing {csv_file.split("/")[-1]} to read files table') 
    spark.createDataFrame([[csv_file.split('/')[-1]]], READFILE_SCHEMA).createOrReplaceTempView('readfile')
    spark.sql('SELECT csvfile FROM readfile').write.mode('append') \
                                  .format('bigquery') \
                                  .option('table', DB_READFILES) \
                                  .save()
    logging.info(f'END: Writing {csv_file.split("/")[-1]} to read files table') 
    #### END: Record processed file ####


## End Spark Job

## Join FILES_TO_PROCESS and FILES_ALREADY_READ in PROCESSED_FILES
#PROCESSED_FILES = FILES_ALREADY_READ + FILES_TO_PROCESS

#write_txt_to_bucket(BUCKET, 'control/read_files.txt', PROCESSED_FILES)
            
#write_txt_to_bucket('cloud-computing-2122-bjr', 'control/read_files.txt', PROCESSED_FILES)