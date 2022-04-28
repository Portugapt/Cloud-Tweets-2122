# Service: Random

- [Service: Random](#service-random)
  - [Service Manifest](#service-manifest)
  - [Deployments Manifest](#deployments-manifest)
    - [Front Flask API](#front-flask-api)
    - [Back Random Language Query Service](#back-random-language-query-service)
  - [Create Protobufs](#create-protobufs)
    - [RandomFront](#randomfront)
    - [RandomLang](#randomlang)
    - [RandomTimeinterval](#randomtimeinterval)
  - [Create, Tag and Push images to Artifact Registry](#create-tag-and-push-images-to-artifact-registry)
    - [Create the images](#create-the-images)
    - [Tag and push the images](#tag-and-push-the-images)
  - [Create Secret for Bigquery connections](#create-secret-for-bigquery-connections)
  - [Apply the deployments](#apply-the-deployments)

This service implements an API to two different services:

* Random Tweet by Interval
* Random Tweet by Language

Going to /random, should route to the Flask service in here, and it's this service job to route to the two other services.

## Service Manifest


> The manifest specified the port (`nodePort`) that should be reserved at every cluster node
> This port must be in the interval 30000-32767. No other service can use this same port. If we don’t specify a nodePort the Kubernetes control plane allocates a port from a range specified by `--service-node-port-range` flag. Each node proxies that port (the same port number on every Node) into your Service. The `nodePort` is open for TCP connections using the http protocol.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: random-svc
spec:
  selector:
    app: random
    version: one
  ports:
  - protocol: TCP
    port: 60100
    targetPort: 60100
---
apiVersion: v1
kind: Service
metadata:
  name: random-lang-svc
spec:
  selector:
    app: random-lang
    version: one
  ports:
  - protocol: TCP
    port: 60110
---
apiVersion: v1
kind: Service
metadata:
  name: random-time-svc
spec:
  selector:
    app: random-time
    version: one
  ports:
  - protocol: TCP
    port: 60120
```


## Deployments Manifest

### Front Flask API

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: random-deployment-v1
spec:
  selector:
    matchLabels:
      app: random
      version: one
  replicas: 3
  template:
    metadata:
      labels:
        app: random
        version: one
    spec:
      containers:
      - name: random
        image: "europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/randomflask:latest"
```

### Back Random Language Query Service

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: random-lang-deployment-v1
spec:
  selector:
    matchLabels:
      app: random-lang
      version: one
  replicas: 3
  template:
    metadata:
      labels:
        app: random-lang
        version: one
    spec:
      containers:
      - name: random-lang
        image: "europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/randomlang:latest"
```

## Create Protobufs

### RandomFront

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto
            
python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/tweetLangService.proto

python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/tweetTimeService.proto
```

### RandomLang

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto

python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/tweetLangService.proto
```


### RandomTimeinterval

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto

python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/tweetTimeService.proto
```

## Create, Tag and Push images to Artifact Registry

### Create the images

```bash
docker build . -f random-front/Dockerfile -t randomflask:2.0

docker build . -f random-lang/Dockerfile -t randomlang:3.0

docker build . -f random-timeinterval/Dockerfile -t randomtime:1.0
```

There's a problem, in the manifest of random-front, it should recieve the env `RANDOMLANG_HOST` AND `RANDOMTIME_HOST`. It does from receive them from the ConfigMap

### Tag and push the images

```bash
docker tag randomflask:2.0 \
europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/randomflask:latest

docker push europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/randomflask:latest
```

```bash
docker tag randomlang:3.0 \
europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/randomlang:latest

docker push europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/randomlang:latest
```

```bash
docker tag randomtime:2.0 \
europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/randomtime:latest

docker push europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/randomtime:latest
```

## Create Secret for Bigquery connections

```bash
kubectl create secret generic bq-key --from-file=key.json=credentials/bq-credentials.json
```

## Apply the deployments