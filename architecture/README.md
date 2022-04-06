# Architecture

- [Architecture](#architecture)
  - [Structure](#structure)
  - [Services](#services)
  - [Databases](#databases)
  - [ETL](#etl)
    - [How?](#how)
  - [Containers](#containers)
    - [Description](#description)
    - [Connections](#connections)
  - [Diagram](#diagram)
- [Google cloud console commands](#google-cloud-console-commands)
  - [Install SDK's](#install-sdks)
    - [gsutil](#gsutil)
  - [bq](#bq)
  - [Create Google Storage Bucket](#create-google-storage-bucket)
  - [Setting up credentials](#setting-up-credentials)
  - [Create Cloud Storage Bucket](#create-cloud-storage-bucket)
    - [Send read_files.txt to Bucket](#send-read_filestxt-to-bucket)
    - [Send CSV's to Bucket](#send-csvs-to-bucket)
  - [Create BigQuery Database](#create-bigquery-database)
  - [Dataproc Cluster Creation](#dataproc-cluster-creation)
    - [Dataproc Job Submit](#dataproc-job-submit)

## Structure

* Authentication  
https://dev.to/behalf/authentication-authorization-in-microservices-architecture-part-i-2cn0

* Review how microservices work together.
* If adding auth, how to make auth db and microservice?
  - https://stackoverflow.blog/2021/10/06/best-practices-for-authentication-and-authorization-for-rest-apis/
  - https://grpc.io/docs/guides/auth/
  - https://medium.com/tech-tajawal/microservice-authentication-and-authorization-solutions-e0e5e74b248a
* Logging Microservices?
  * https://logz.io/blog/a-practical-guide-to-kubernetes-logging/
* Base microservices are Connectors. (To DBs)

## Services

* Cloud Storage
* BigQuery
* Dataproc
* GKE (+ Cloud Computing)
* Cloud Composer??
  - https://cloud.google.com/architecture/cicd-pipeline-for-data-processing
* Cloud Build (CI/CD) (https://cloud.google.com/docs/ci-cd)
* Artifact Registry
* Jenkins ? (https://cloud.google.com/architecture/jenkins-on-kubernetes-engine)

## Databases

* Users (BigQuery)
* Tweets (BigQuery)
* Hashtags (BigTable) ???
* Avaliable Tweet Languages

## ETL

Spark Job that reads the not-yet read CSV files available in the Bucket.  
Consistency requirements:

* Upload not yet in DB Tweets
* Upload not yet in DB Users
* Update Already in DB Users (If name change or description)
* Add Language if not already in Language DB.

### How?

* 0: Check which CSV's havent been read
  * https://stackoverflow.com/questions/48279061/gcs-read-a-text-file-from-google-cloud-storage-directly-into-python
* 1: Read the CSV(s)
  * https://cloud.google.com/storage/docs/listing-objects#storage-list-objects-python
* 2: Query db_users
* 3: Structure into 3/4 spark tables
* 3-1: Check if any user needs updating
* 3-2: Control flow to update such users, separating tables
* 4: Populate with new data the dbs
* 4-1: Update with new data the users data
* 5: Record csv as read in control file

## Containers

### Description

* (A) BD Request: Random Tweet Languague
  * Connects to Languages DB, and randomly selects one of the avaliable.
* (B) BD Request: Tweet time interval
  * Receives a time interval request, and retrieves all tweets from that time interval from the Tweets DB.
* (C) BD Request: User Information
  * With an UserID, retrieves all information User DB information about that user.
* (D) Transform Lang+TimeInterval
  * Requests both necessary dbs, and transforms the data to a presentable structure.
* (E) Passei à frente sem querer.
* (F) Transform Search String Request
  * Structures the string list, and can provide extra information about the string, for example the languages appearing in the search; the word frequency of the all the texts; Vagueness (Only that word, lots of words?)
* (G) Transform Location+TimeInteval
  * Receives location + timeinterval, and requests BD containers, location + time interval if day > 1, because filtering in the container might be heavy; TimeInterval(B) if request filter load is not heavy.
* (H) BD Request: custom query to tweets database
  * Basically only functions to query the data in a custom manner. Depending on the container asking, he will request the data, and the asking container takes of the rest. Use in exceptional situations, can be heavy on the table.
* (I) Transform Language
  * Serves as control for query request, and transforms the list of langs to a presentable structure
* (J) Transform Tweets by username
  * Serves as flow to database requests, informs about one or more userID with same username, and structures data for response
* (K) BD Request: UserID
  * Requests all information about a UserID to the database
* (L) Manage bd_tweets
  * Only function is throw a requested custom query to update, create or delete tweet
* (M) Manage bd_users
  * Only function is throw a requested custom query to update, create or delete user
* (Z) Any amount of containers needed as frontend to report backend containers responses.

### Connections

-----

* Selects a random tweet by language:
  * (A):bd_langs
    * Request: Lang
    * 200: [Lang] or Rand(List) #list or string
  * (B):bd_tweets
    * Request:TimeInterval
    * 200:[Tweet] #list
  * (D):A+B
    * Request:Lang+TimeInterval
    * 200:FilteredTweets #list
  * (Z):D
    * Request:CURL
    * 200:CustomResponse1

-----

* Selects a random tweet by time interval
  * (B):bd_tweets
    * Request:TimeInterval
    * 200:[Tweet] #list
  * (D):B
    * Request:TimeInterval
    * 200:FilteredTweets #list
  * (Z):D
    * Request:CURL
    * 200:CustomResponse2 #String

-----

* List of tweets that contain search string
  * (B):bd_tweets
    * Request:SearchString
    * 200:[Tweets] #list
  * (F):B
    * Request:SearchString
    * 200:[Tweets]+METADATA #eg:word frequency
  * (Z):F
    * Request:CURL
    * 200:CustomResponse3

-----

* List of location by time interval
  * IF TimeInterval < 1day; (B_1):bd_tweets
    * Request:TimeInterval
    * 200:[Tweet] #list
  * IF TimeInterval > 1day; (B_2):bd_tweets
    * Request:Location+TimeInterval
    * 200:[Tweet] #list
  * (G):(B_1/B_2)
    * Request:Location+TimeInterval
    * 200:[Tweet] #list
  * (Z):G
    * Request:CURL
    * 200:CustomResponse4

-----

* List of spoken languages by time interval
  * IF TimeInterval < 1day; (B):bd_tweets
    * Request:TimeInterval
    * 200:[Tweet] #list
  * IF TimeInterval > 1day; (H):bd_tweets
    * Request:CustomQuery
    * 200:QueryReadyResult
  * (I):B/H
    * Request:TimeInterval
    * 200:[Lang] #list
  * (Z):I
    * Request:CURL
    * 200:CustomResponse5

-----

* List all tweets from username
  * (C):bd_users
    * Request:Username
    * 200:AllUserData
  * (K):bd_tweets
    * Request:UserID
    * 200: [Tweet] #list
  * (J):C+B
    * Request:Username --> UserIDTweets
    * 200: [Tweet] #list or two userID's with same username
  * (Z):J
    * Request:CURL
    * 200: CustomResponse6

-----

* Delete Tweet
  * (L):bd_tweets
    * Request:DeleteTweet
    * 200:200
  * E:db_auth
    * 
  * (Z):L
    * Request:TweetID
    * 200:200

-----

* Add Tweet
  * (L):bd_tweets
    * Request:CreateTweet
    * 200:200
  * (Z):L
    * Request:TweetID
    * 200:200

-----

Falta:

* Autenticação (Em link acima)
* Logging (Em link acima)

## Diagram

Construir o diagrama

* Containers + Ligações
  * Entre containers
  * Com bases de dados
* Dentro de Kubernetes (Inc. Namespaces)
* Ligações a logging e auth ??
* Tipo de gateway ??
* Tipo de orquestração
  * CI/CD
  * Deploy
  * Manutenção para ETL
  * VPC/s;Istios;etc
* Outros serviços
  * GS, Dataproc, Bigquery, ...

# Google cloud console commands

## Install SDK's

### gsutil

https://cloud.google.com/storage/docs/gsutil_install#debian-and-ubuntu

```bash
sudo apt-get install gcc python-dev python-setuptools libffi-dev
```

```bash
sudo pip install gsutil
```

Add gsutil command
```bash
export PATH=${PATH}:$usr/bin/gsutil
```

Run
```bash
gsutil config
```
To login into the account. All should be set now.

## bq

```bash
sudo snap install google-cloud-cli --classic
```

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
export GOOGLE_APPLICATION_CREDENTIALS="credentials/credentials-gs.json"
```

## Create Cloud Storage Bucket

```bash
gsutil mb -l EUROPE-WEST1 -c STANDARD gs://cloud-computing-2122-bjr
```

### Send read_files.txt to Bucket

https://cloud.google.com/storage/docs/gsutil/commands/cp

```bash
gsutil cp data/read_files.txt gs://cloud-computing-2122-bjr/control/
```

### Send CSV's to Bucket
+
## Create BigQuery Database

```bash
bq --location=europe-west1 mk \
--dataset \
cadeira-nuvem-2122:bq_cloud_2122
```


## Dataproc Cluster Creation

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
  --project cadeira-nuvem-2122
```

### Dataproc Job Submit

```bash
gcloud dataproc jobs submit pyspark gs://cloud-computing-2122-bjr/spark-jobs/write_to_bigquery.py \
    --cluster=cloud-2122-etl-spark \
    --region=europe-west1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest.jar
```

https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example#pyspark