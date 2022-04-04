from pyspark.sql import SparkSession
from google.cloud import storage

BUCKET = 'cloud-computing-2122-bjr'

# Read txt file of already processed CSV's
def read_txt_blob(bucket_name, destination_file_name):
    # https://stackoverflow.com/questions/48279061/gcs-read-a-text-file-from-google-cloud-storage-directly-into-python
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(destination_file_name)
    read_file = blob.download_as_text(encoding="utf-8")
    # Log instead of print
    """
    print(
        "Loaded from bucket {} to local file {}.".format(
            bucket_name, destination_file_name
        )
    )
    """
    return read_file.split('\n')

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


FILES_ALREADY_READ = read_txt_blob(BUCKET, 'control/read_files.txt')
DATA_IN_BUCKET = list_blobs_with_prefix(BUCKET, 'data/')

FILES_TO_PROCESS = [FILE for FILE in DATA_IN_BUCKET if FILE not in FILES_ALREADY_READ]


## Spark Job

spark = SparkSession \
  .builder \
  .appName('spark-ETL-Tweets') \
  .getOrCreate()



## End Spark Job

## Join FILES_TO_PROCESS and FILES_ALREADY_READ in PROCESSED_FILES
PROCESSED_FILES = []

# Update txt file after data is processed
# https://stackoverflow.com/questions/43682521/writing-data-to-google-cloud-storage-using-python
def write_txt_to_bucket(bucket_name, destination_file_name, files_list):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_file_name) 
    ## Use bucket.get_blob('path/to/existing-blob-name.txt') to write to existing blobs
    with blob.open(mode='w') as f:
        f.write('\n'.join(files_list))
            
write_txt_to_bucket('cloud-computing-2122-bjr', 'control/read_files.txt', PROCESSED_FILES)