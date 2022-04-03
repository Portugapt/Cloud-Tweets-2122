- [Architecture](#architecture)
  - [Services](#services)
  - [Databases](#databases)
  - [ETL](#etl)
    - [How?](#how)
  - [Containers](#containers)
    - [Description](#description)
    - [Connections](#connections)
  - [Diagram](#diagram)
- [Google cloud console commands](#google-cloud-console-commands)
  - [Create Google Storage Bucket](#create-google-storage-bucket)
  - [Setting up credentials](#setting-up-credentials)
  - [Create Cloud Storage Bucket](#create-cloud-storage-bucket)
  - [Create BigQuery Database](#create-bigquery-database)
  - [Create BigQuery Tables](#create-bigquery-tables)

# Architecture

Authentication   
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
* Jenkins (https://cloud.google.com/architecture/jenkins-on-kubernetes-engine)

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
## Containers

### Description

* (A) Select Random Tweet Languague
  * Connects to Languages DB, and randomly selects one of the avaliable.
* (B) Filter Tweet time interval
  * Receives a time interval request, and retrieves all tweets from that time interval from the Tweets DB.
* (C) Retrieve User Information
  * With an UserID, retrieves all information User DB information about that user.
* (D) Transform Lang+TimeInterval
  * Requests both necessary dbs, and transforms the data to a presentable structure.
* (E)
* (F) Transform Search String Request
  * Structures the string list, and can provide extra information about the string, for example the languages appearing in the search; the word frequency of the all the texts; Vagueness (Only that word, lots of words?)
* (G) Transform Location+TimeInteval
  * Recieves location + timeinterval, and requests BD containers, location + time interval if day > 1, because filtering in the container might be heavy; TimeInterval(B) if request filter load is not heavy.
* (H) Request custom query to tweets database
  * Basically only functions to query the data in a custom manner. Depending on the container asking, he will structure the data. Use in exceptional situations, can be heavy on the table.
* (I) Transform Language
  * Serves as control for query request, and transforms the list of langs to a presentable structure

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
    * Request:TimeInterval
    * 200:CustomResponse5
-----
* List all tweets from username
  * (C):bd_users
    * Request:Username
    * 200:AllUserData
  * (B):bd_tweets
    * Request:UserID #Another Container NOT B
    * 200: [Tweet] #list
  * (J)
## Diagram


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
