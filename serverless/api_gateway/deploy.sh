# Create API
gcloud api-gateway apis create ukraine-api

# Create API config
gcloud api-gateway api-configs create ukraine-functions-config --api=ukraine-api --openapi-spec=./config.yaml --backend-auth-service-account=474801923734-compute@developer.gserviceaccount.com

# Create API Gateway
gcloud api-gateway gateways create ukraine-api-gateway --location=europe-west1 --api-config=ukraine-functions-config --api=ukraine-api
