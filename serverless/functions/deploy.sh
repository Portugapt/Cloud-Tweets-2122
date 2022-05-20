# Create secret access to biquery key
gcloud secrets create key_bigquery_access --replication-policy="automatic"
gcloud secrets add-iam-policy-binding key_bigquery_access --member="serviceAccount:cadeira-nuvem-2122@appspot.gserviceaccount.com" --role="roles/secretmanager.secretAccessor"
gcloud secrets versions add key_bigquery_access --data-file="./keys/pythonBigQuery_credentials.json"


# Deploy functions

gcloud functions deploy admin_add_tweet --source ./admin-add-tweet --trigger-http --runtime python37 --region europe-west1 --quiet --set-secrets '/keys/BigQuery_credentials.json=key_bigquery_access:latest' --env-vars-file .env-admin.yaml &

gcloud functions deploy admin_delete_tweet --source ./admin-delete-tweet --trigger-http --runtime python37 --region europe-west1 --quiet --set-secrets '/keys/BigQuery_credentials.json=key_bigquery_access:latest' --env-vars-file .env-admin.yaml &

gcloud functions deploy auth --source ./auth --trigger-http --runtime python37 --allow-unauthenticated --region europe-west1 --quiet --set-secrets '/keys/BigQuery_credentials.json=key_bigquery_access:latest' --env-vars-file .env-admin.yaml &

gcloud functions deploy clear_tweet_list --source ./clear-tweet-list --trigger-http --runtime python37 --allow-unauthenticated --region europe-west1 --quiet &

gcloud functions deploy list_tweet_language --source ./list-tweet-language --trigger-http --runtime python37 --region europe-west1 --quiet --set-secrets '/keys/BigQuery_credentials.json=key_bigquery_access:latest' --env-vars-file .env-list.yaml &

gcloud functions deploy list_tweet_location --source ./list-tweet-location --trigger-http --runtime python37 --region europe-west1 --quiet --set-secrets '/keys/BigQuery_credentials.json=key_bigquery_access:latest' --env-vars-file .env-list.yaml &

gcloud functions deploy list_tweet_random --source ./list-tweet-random --trigger-http --runtime python37 --region europe-west1 --quiet --set-secrets '/keys/BigQuery_credentials.json=key_bigquery_access:latest' --env-vars-file .env-list.yaml &

gcloud functions deploy list_tweet_search --source ./list-tweet-search --trigger-http --runtime python37 --region europe-west1 --quiet --set-secrets '/keys/BigQuery_credentials.json=key_bigquery_access:latest' --env-vars-file .env-list.yaml &

gcloud functions deploy list_tweet_username --source ./list-tweet-username --trigger-http --runtime python37 --region europe-west1 --quiet --set-secrets '/keys/BigQuery_credentials.json=key_bigquery_access:latest' --env-vars-file .env-list.yaml &