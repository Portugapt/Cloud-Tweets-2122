

https://www.pulumi.com/registry/packages/gcp/api-docs/compute/address/


https://www.pulumi.com/registry/packages/gcp/api-docs/compute/forwardingrule/


load_balancing_scheme = EXTERNAL


* https://cloud.google.com/load-balancing/docs/https/setting-up-https-serverless
* https://cloud.google.com/api-gateway/docs/gateway-serverless-neg
  * https://cloud.google.com/api-gateway/docs/gateway-load-balancing

É preciso um secret do secret manager

* Definir a API com o provider sendo a front?
* Ou então é o URL MAP

```bash
service-run-backend@cadeira-nuvem-2122.iam.gserviceaccount.com 
```

Tutorial: 
https://cloud.google.com/api-gateway/docs/secure-traffic-gcloud

create api

```bash
gcloud api-gateway api-configs create api-run-config-v2 \
--api=cloud-run-tweets-api \
--openapi-spec=api-v2.yaml \
--project=cadeira-nuvem-2122 \
--backend-auth-service-account=service-run-backend@cadeira-nuvem-2122.iam.gserviceaccount.com 
```

update (CANT)  
https://cloud.google.com/api-gateway/docs/creating-api-config#updating-an-api-config  
https://cloud.google.com/api-gateway/docs/creating-api-config#deleting-an-api-config

check api

```bash

gcloud api-gateway api-configs describe api-run-config \
--api=cloud-run-tweets-api \
--project=cadeira-nuvem-2122
```

Deploying an API Gateway

```bash
gcloud api-gateway gateways create cloud-run-gateway \
  --api=cloud-run-tweets-api --api-config=api-run-config \
  --location=europe-west1 --project=cadeira-nuvem-2122
```

describe

```bash
gcloud api-gateway gateways describe cloud-run-gateway \
  --location=europe-west1 --project=cadeira-nuvem-2122
```

create Serverless NEG

```bash
gcloud beta compute network-endpoint-groups create cloud-run-tweets \
  --region=europe-west1 \
  --network-endpoint-type=serverless \
  --serverless-deployment-platform=apigateway.googleapis.com \
  --serverless-deployment-resource=cloud-run-gateway
```

Create backend service

```bash
gcloud compute backend-services create backend-tweets \
--global
```


```bash
gcloud compute backend-services add-backend backend-tweets \
--global \
--network-endpoint-group=cloud-run-tweets \
--network-endpoint-group-region=europe-west1
```

create url-map  

```bash
gcloud compute url-maps create url-map-tweets \
--default-service backend-tweets
```

create certificate  

https://www.ibm.com/docs/en/api-connect/10.0.1.x?topic=overview-generating-self-signed-certificate-using-openssl

```bash
openssl req -newkey rsa:2048 -nodes -keyout self-key.pem -x509 -days 365 -out self-ssl.pem
```

```bash
gcloud compute ssl-certificates create ssl-self-managed \
  --certificate ../certificates/self-ssl.pem \
  --private-key ../certificates/self-key.pem
```

```bash
gcloud compute target-https-proxies create https-proxy-tweets \
--ssl-certificates=ssl-self-managed \
--url-map=url-map-tweets
```

forward rule

```bash
gcloud compute forwarding-rules create tweets-fwr \
  --target-https-proxy=https-proxy-tweets \
  --global \
  --ports=443 \
  --address=34.96.113.22
```