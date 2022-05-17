
## Launch test function
gcloud functions deploy test_function --source . --trigger-http --runtime python37 --allow-unauthenticated