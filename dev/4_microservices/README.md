# Microservices infrastructure

- [Microservices infrastructure](#microservices-infrastructure)
  - [Config kubectl](#config-kubectl)
  - [Artifact Registry Repository](#artifact-registry-repository)
  - [Create GKE Cluster](#create-gke-cluster)
  - [Connect to GKE Cluster](#connect-to-gke-cluster)
  - [Create Secret for Bigquery connections](#create-secret-for-bigquery-connections)
  - [Ingress](#ingress)
    - [Install nginx-Ingress](#install-nginx-ingress)
    - [Get the External IP](#get-the-external-ip)
    - [V2](#v2)
  - [Other notes](#other-notes)
    - [1. With HTTPRoute](#1-with-httproute)



## Config kubectl 


https://cloud.google.com/sdk/docs/install#deb

https://cloud.google.com/config-connector/docs/how-to/install-upgrade-uninstall

[Configurate kubectl to GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl)

```bash
apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
```

Assumes I've already created the cluster described below.

```bash
gcloud container clusters get-credentials twitter-services-cluster
```

## Artifact Registry Repository

Create the repository
```bash
gcloud artifacts repositories create cloud-microservices \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Cloud Course Microservices Repository"
```

Configure authentication
```bash
gcloud auth configure-docker europe-west1-docker.pkg.dev
```

> The command updates your Docker configuration. You can now connect with Artifact Registry in your Google Cloud project to push and pull images. [REF](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images)

## Create GKE Cluster

```bash
gcloud beta container --project "cadeira-nuvem-2122" clusters create "twitter-services-cluster" --zone "europe-west1-d" --no-enable-basic-auth --cluster-version "1.21.6-gke.1503" --release-channel "regular" --machine-type "e2-medium" --image-type "COS_CONTAINERD" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/bigquery","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --max-pods-per-node "110" --num-nodes "3" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/cadeira-nuvem-2122/global/networks/default" --subnetwork "projects/cadeira-nuvem-2122/regions/europe-west1/subnetworks/default" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --enable-shielded-nodes --node-locations "europe-west1-d"
```

## Connect to GKE Cluster

```bash
gcloud container clusters get-credentials twitter-services-cluster --zone europe-west1-d --project cadeira-nuvem-2122
```

## Create Secret for Bigquery connections

```bash
kubectl create secret generic bq-key --from-file=key.json=credentials/bq-credentials.json
```

## Ingress

### Install nginx-Ingress

https://cloud.google.com/community/tutorials/nginx-ingress-gke

On the cloud shell:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

```bash
helm install nginx-ingress ingress-nginx/ingress-nginx
```

This should deploy the nginx-ingress controller.

### Get the External IP

```bash
kubectl get deployment nginx-ingress-ingress-nginx-controller

kubectl get service nginx-ingress-ingress-nginx-controller
```



### V2 

For the specific requests to be served by correct services inside the cluster, it's necessary to define an Ingress, or a Load Balancer, that exposes the cluster with an external IP.

Taken from [here](https://cloud.google.com/kubernetes-engine/docs/how-to/load-balance-ingress)

The Lab guide is also helpful.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  - host: INGRESS_IP.nip.io
    http:
      paths:
      - path: /random/
        pathType: Prefix
        backend:
          service:
            ## Service manifest in the random service folder
            name: random-svc
            port:
              number: 60100
      - path: /search/
        pathType: Prefix
        backend:
          service:
            ## Service manifest in the random service folder
            name: search-svc
            port:
              number: 60200
```

## Other notes

Reminders: 
* [FQDN](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
* 

How?
1. HTTPRoute
   * https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-gateways#store-route
2. Ingress-nginx
    * https://cloud.google.com/community/tutorials/nginx-ingress-gke
    * https://kubernetes.github.io/ingress-nginx/deploy/#gce-gke
3. Ingress + HTTP Load balancer
   * https://cloud.google.com/kubernetes-engine/docs/tutorials/http-balancer
   * https://cloud.google.com/kubernetes-engine/docs/how-to/load-balance-ingress

### 1. With HTTPRoute

```yaml
kind: HTTPRoute
apiVersion: gateway.networking.k8s.io/v1alpha2
metadata:
  name: store-german-route
  labels:
    gateway: internal-http
spec:
  hostnames:
  - "store.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /de
    backendRefs:
    - kind: Service
      name: store-german
      port: 8080
```

I can define the host-name with services like in [here](https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/courses/ak8s/v1.1/GKE_Services/dns-demo.yaml)