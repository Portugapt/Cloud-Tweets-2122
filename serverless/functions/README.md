
## Launch test function
gcloud functions deploy test_function --source . --trigger-http --runtime python37 --allow-unauthenticated



## Create key in secret manager
gcloud secrets create key_bigquery_access --replication-policy="automatic"

gcloud secrets versions add key_bigquery_access --data-file="/path/to/file.txt"


gcloud functions add-iam-policy-binding clear_tweet_list --region=europe-west1 --member='serviceAccount:gs-service@cadeira-nuvem-2122.iam.gserviceaccount.com' --role='roles/cloudfunctions.invoker'