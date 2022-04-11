# Dataproc ETL

## Dataproc Cluster Creation

Create Temprary dataproc bucket for spark jobs

```bash
gsutil mb -l EUROPE-WEST1 -c STANDARD gs://cloud-computing-2122-dataproc-temp
```

https://github.com/GoogleCloudDataproc/initialization-actions/tree/master/connectors

```bash
gcloud dataproc clusters create cloud-2122-etl-spark \
  --region europe-west1 \
  --zone europe-west1-c \
  --master-machine-type n1-standard-2 \
  --master-boot-disk-size 100 \
  --num-workers 2 \
  --worker-machine-type n1-standard-2 \
  --worker-boot-disk-size 50 \
  --image-version 2.0-debian10 \
  --initialization-actions gs://goog-dataproc-initialization-actions-europe-west1/connectors/connectors.sh \
  --metadata bigquery-connector-version=1.2.0 \
  --metadata spark-bigquery-connector-version=0.21.0 \
  --metadata GCS_CONNECTOR_VERSION=2.2.2 \
  --metadata='PIP_PACKAGES=pandas==0.23.0' \
  --project cadeira-nuvem-2122
```

## Dataproc Job Submit

Copy the file to gcs

```bash
gsutil cp loadDataToBigquery.py gs://cloud-computing-2122-bjr/spark-jobs/
```

```bash
gcloud dataproc jobs submit pyspark gs://cloud-computing-2122-bjr/spark-jobs/loadDataToBigquery.py \
    --cluster=cloud-2122-etl-spark \
    --region=europe-west1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest.jar
```

https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example#pyspark