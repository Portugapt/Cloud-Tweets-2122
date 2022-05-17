
## Create API
gcloud api-gateway apis create test-list-api --project=cadeira-nuvem-2122

## Create Config
gcloud api-gateway api-configs create test-list-config --api=test-list-api --openapi-spec=config.yaml --project=cadeira-nuvem-2122 --backend-auth-service-account=service-run-backend@cadeira-nuvem-2122.iam.gserviceaccount.com

## Create Gateway
gcloud api-gateway gateways describe GATEWAY_ID --location=GCP_REGION --project=PROJECT_ID --api-config=API_CONFIG


