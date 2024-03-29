#!/usr/bin/env python

import logging
from pyspark.sql import SparkSession
from google.cloud import storage
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, TimestampType, ArrayType, LongType

logging.basicConfig(level=logging.INFO)

BUCKET = 'cloud-computing-2122-bjr'
BUCKET_LINK = 'gs://cloud-computing-2122-bjr'
TEMP_BUCKET = 'cloud-computing-2122-dataproc-temp'

DB_USERS = 'cadeira-nuvem-2122:bq_cloud_2122.db_users'
DB_TWEETS = 'cadeira-nuvem-2122:bq_cloud_2122.db_tweets'
DB_READFILES = 'cadeira-nuvem-2122:bq_cloud_2122.db_readfiles'


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

USERS_SCHEMA = StructType([ \
    StructField("userId",LongType(),False), \
    StructField("usercreatedts",TimestampType(),False), \
    StructField("username",StringType(),False), \
    StructField("acctdesc",StringType(),True), \
    StructField("n_following", IntegerType(), True), \
    StructField("n_followers", IntegerType(), True), \
    StructField("n_totaltweets", IntegerType(), True), \
  ])

READFILE_SCHEMA = StructType([StructField('csvfile', StringType(), False)])

# Read txt file of already processed CSV's
"""
def read_txt_blob(bucket_name, destination_file_name):
    # https://stackoverflow.com/questions/48279061/gcs-read-a-text-file-from-google-cloud-storage-directly-into-python
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(destination_file_name)
    read_file = blob.download_as_text(encoding="utf-8")
    # Log instead of print
    
    print(
        "Loaded from bucket {} to local file {}.".format(
            bucket_name, destination_file_name
        )
    )
    
    return read_file.split('\n')
"""

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

### TODO 
## PASSAR TXT PARA TABLE BIGQUERY

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
FILES_ALREADY_READ = [row for row in READFILES]
#FILES_ALREADY_READ = read_txt_blob(BUCKET, 'control/read_files.txt')

# Create list of files in the data bucket
DATA_IN_BUCKET = list_blobs_with_prefix(BUCKET, 'data/')

# Create list of files to process
FILES_TO_PROCESS = [f'data/{FILE}' for FILE in DATA_IN_BUCKET if FILE not in FILES_ALREADY_READ]


#   .config('spark.jars', 'gs://hadoop-lib/gcs/gcs-connector-hadoop2-latest.jar,gs://spark-lib/bigquery/spark-bigquery-latest.jar') \


print(FILES_ALREADY_READ)
print(DATA_IN_BUCKET)
print(FILES_TO_PROCESS)

# Get the user data
db_Users = spark.read.format('bigquery') \
  .option("table",DB_USERS) \
  .load()
dfUsers = db_Users.select("userId")
dfUsers.write.mode("append").saveAsTable("ALL_USERS")

for csv_file in FILES_TO_PROCESS:
    ## DOES NOT WORK
    ##sc = SparkContext.getOrCreate()
    ##rdd_csv = sc.wholeTextFiles(f"{BUCKET_LINK}/{csv_file}")
    ##rdd_csv.collect()
    ## WORKS - BUT DOES IT WORK FOR MULTIPLE FILES READ?
    logging.info(f'Going to read csv_file {csv_file} from bucket')
    csv_data = (spark
                .read
                .format("csv")
                .option("wholeFile", True)
                .option("multiline",True)
                .option("header", True)
                .option("inferSchema", "true")
                .option("dateFormat", "yyyy-MM-dd")
                .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")
                .schema(GLOBAL_SCHEMA)
                .load(f"{BUCKET_LINK}/{csv_file}"))
    logging.info(f'Read csv_file {csv_file} from bucket sucessfully')
    csv_data.createOrReplaceTempView("DATA_FILE")
    logging.info(f'Created Global data temp view')
    #csv_file.printSchema()


    #### START: USER DATA ####
    ## Duplicated Users Data has the information for update. When it's implemented, should be the table giving the data to update users
    logging.info(f'START: DROPING DUPLICATEED_USERS table if exists')
    spark.sql("DROP TABLE IF EXISTS DUPLICATED_USERS")
    logging.info(f'END: DROPING DUPLICATEED_USERS table if exists')
    logging.info(f'START: Creating DUPLICATEED_USERS table')
    spark.sql("""SELECT A.userId FROM DATA_FILE A INNER JOIN ALL_USERS B ON A.userId == B.UserId""").write.mode("overwrite").saveAsTable("DUPLICATED_USERS")
    logging.info(f'SUCCESS: Creating DUPLUCATED_USERS table')
    
    ### NEW_USER_DATA is the table that's thrown into bigquery
    #spark.sql("""SELECT DISTINCT
    #                A.userId, 
    #                A.usercreatedts, 
    #                A.username, 
    #                A.acctdesc, 
    #                A.n_following, 
    #                A.n_followers, 
    #                A.n_totaltweets 
    #            FROM DATA_FILE A INNER JOIN DUPLICATED_USERS B ON A.userId <> B.UserId""").createOrReplaceTempView("NEW_USER_DATA")
    
    ## This is the control table in the script, that if several CSV files are loaded, the chances of an user being loaded twice are nullified.
    logging.info(f'START: Populating ALL_USERS Table')
    spark.sql("""INSERT INTO TABLE ALL_USERS SELECT userId FROM DATA_FILE""")
    logging.info(f'END: Populating ALL_USERS Table')
    
    logging.info(f'START: Populate Bigquery with user data')
    spark.sql("""SELECT DISTINCT A.userId, 
                    A.usercreatedts, 
                    A.username, 
                    A.acctdesc, 
                    A.n_following, 
                    A.n_followers, 
                    A.n_totaltweets 
                    FROM DATA_FILE A, DUPLICATED_USERS B
                    WHERE A.userId <> B.userId""").write.mode('append') \
                                                  .format('bigquery') \
                                                  .option('table', DB_USERS) \
                                                  .save()
    logging.info(f'END: Populate Bigquery with user data')                                            

    ### TODO ###
    #UPDATE USER DATA THAT'S IN DUPLICATES
    # CHANGE USER_DATA_TEST TO ALL_USERS
    #### END: USER DATA ####

    #### START: TWEETS DATA ####
    logging.info(f'START: Populate Bigquery with Tweets data') 
    spark.sql("""SELECT
                tweetId, 
                tweetcreatedts, 
                userId, 
                location, 
                language, 
                retweetcount, 
                favouritecount,
                tweettext,
                hashtags,
                coordinates,
                extractedts
                FROM DATA_FILE""").write.mode('append') \
                                  .format('bigquery') \
                                  .option('table', DB_TWEETS) \
                                  .save()
    logging.info(f'END: Populate Bigquery with Tweets data') 

    #### END: TWEETS DATA ####

    #### START: Record processed file ####
    logging.info(f'START: Writing {csv_file.split("/")[-1]} to read files table') 
    df = spark.createDataFrame([[csv_file.split('/')[-1]]], READFILE_SCHEMA)
    df.show() 
    df.createOrReplaceTempView('readfile')
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