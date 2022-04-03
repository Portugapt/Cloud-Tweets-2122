- [Architecture](#architecture)
- [Google cloud console commands](#google-cloud-console-commands)
  - [Create Google Storage Bucket](#create-google-storage-bucket)
  - [Setting up credentials](#setting-up-credentials)
  - [Create Cloud Storage Bucket](#create-cloud-storage-bucket)
  - [Create BigQuery Database](#create-bigquery-database)
  - [Create BigQuery Tables](#create-bigquery-tables)

# Architecture



# Google cloud console commands

## Create Google Storage Bucket

With the goal of creating the Google Storage bucket, the following commands should do the trick:

On the Google Console:

Set the project:
```bash
gcloud config set project cadeira-nuvem-2122
```

Create service account:
```bash
gcloud iam service-accounts create gs-service
```   


ADD ALL THE NECESSARY ROLES FOR GS AND OTHER SERVICES:
```
gcloud projects add-iam-policy-binding cadeira-nuvem-2122 --member="serviceAccount:gs-service@cadeira-nuvem-2122.iam.gserviceaccount.com" --role=roles/storage.admin

gcloud projects add-iam-policy-binding cadeira-nuvem-2122 --member="serviceAccount:gs-service@cadeira-nuvem-2122.iam.gserviceaccount.com" --role=roles/bigquery.admin
```

Finally, get the credentials to work remotely:
```bash
gcloud iam service-accounts keys create gs-credentials.json --iam-account=gs-service@cadeira-nuvem-2122.iam.gserviceaccount.com
```

And we download it from the console files.


## Setting up credentials

```bash
export GOOGLE_APPLICATION_CREDENTIALS="Scripts/credentials-gs.json"
```

## Create Cloud Storage Bucket

```bash
gsutil mb -l EUROPE-WEST1 -c STANDARD gs://cloud-computing-2122-bjr
```



## Create BigQuery Database

```bash
bq --location=europe-west1 mk \
--dataset \
cadeira-nuvem-2122:bq_cloud_2122
```


## Create BigQuery Tables

Three tables
* Users (BigQuery)
* Tweets (BigQuery)
* Hashtags (BigTable)
