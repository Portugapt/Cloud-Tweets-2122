# BigQuery 

## Send read_files.txt to Bucket

https://cloud.google.com/storage/docs/gsutil/commands/cp

```bash
gsutil cp data/read_files.txt gs://cloud-computing-2122-bjr/control/
```

## Create BigQuery Database

```bash
bq --location=europe-west1 mk \
--dataset \
cadeira-nuvem-2122:bq_cloud_2122
```


## Create Read Files Database

```bash
bq mk \
--table \
--description "Read Files Database" \
--label organization:development \
cadeira-nuvem-2122:bq_cloud_2122.db_readfiles \
db_readfiles_schema.json
```

## Create Global Dataset

```bash
bq mk \
--table \
--description "Global dataset" \
--label organization:development \
cadeira-nuvem-2122:bq_cloud_2122.db_global \
db_global_schema.json
```


## Create Users View

```bash
bq mk \
--use_legacy_sql=false \
--description "Users View" \
--label organization:development \
--project_id cadeira-nuvem-2122  \
--view \
'SELECT
  name,
  number
FROM
  `bigquery-public-data.usa_names.usa_1910_current`
WHERE
  gender = "M"
ORDER BY
  number DESC' \
mydataset.myview
```

## Create Tweets View

```bash
bq mk \
--table \
--description "Tweets Database" \
--label organization:development \
cadeira-nuvem-2122:bq_cloud_2122.db_tweets \
db_tweet_schema.json
```


