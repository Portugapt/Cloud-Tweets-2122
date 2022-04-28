# Search Services

- [Search Services](#search-services)
  - [Implementation](#implementation)
  - [Protobufs](#protobufs)
    - [Search Front](#search-front)
    - [Search by String](#search-by-string)
    - [Search by Username](#search-by-username)
    - [Create, Tag and Push images](#create-tag-and-push-images)
    - [Search Front](#search-front-1)
    - [Search String](#search-string)
    - [Search Username Tweets](#search-username-tweets)
  - [Services](#services)
  - [Deployments](#deployments)
  - [Update](#update)

## Implementation

* Search By String
* Search tweets bu username

## Protobufs

### Search Front

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto
            
python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/searchStringService.proto

python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/searchUserService.proto
```

### Search by String

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto

python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/searchStringService.proto
```

### Search by Username

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto

python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/searchUserService.proto
```

### Create, Tag and Push images


### Search Front

```bash
docker build . -f search_front/Dockerfile -t searchflask:3.0

docker tag searchflask:3.0 \
europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchflask:latest

docker push europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchflask:latest
```

### Search String

```bash
docker build . -f searchString/Dockerfile -t searchstring:2.0

docker tag searchstring:2.0 \
europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchstring:latest

docker push europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchstring:latest
```

### Search Username Tweets

```bash
docker build . -f searchUsername/Dockerfile -t searchusername:1.0

docker tag searchusername:1.0 \
europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchusername:latest

docker push europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchusername:latest
```

## Services

```yaml
apiVersion: v1
kind: Service
metadata:
  name: search-svc
spec:
  selector:
    app: search
    version: one
  ports:
  - protocol: TCP
    port: 60200
    targetPort: 60200
---
apiVersion: v1
kind: Service
metadata:
  name: search-string-svc
spec:
  selector:
    app: search
    version: one
  ports:
  - protocol: TCP
    port: 60210
    targetPort: 60210
---
apiVersion: v1
kind: Service
metadata:
  name: search-username-svc
spec:
  selector:
    app: search-username
    version: one
  ports:
  - protocol: TCP
    port: 60220
    targetPort: 60220
```

## Deployments

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: search-deployment-v1
spec:
  selector:
    matchLabels:
      app: search
      version: one
  replicas: 3
  template:
    metadata:
      labels:
        app: search
        version: one
    spec:
      containers:
      - name: search
        image: "europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchflask:latest"
        env:
            - name: STRING_HOST
              valueFrom:
                configMapKeyRef:
                  name: search-configmap
                  key: string_service_name
            - name: USERNAME_HOST
              valueFrom:
                configMapKeyRef:
                  name: search-configmap
                  key: username_service_name
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: search-string-deployment-v1
spec:
  selector:
    matchLabels:
      app: search-string
      version: one
  replicas: 3
  template:
    metadata:
      labels:
        app: search-string
        version: one
    spec:
      volumes:
      - name: bq-read-key
        secret:
          secretName: bq-key
      containers:
      - name: search-string
        image: "europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchstring:latest"
        volumeMounts:
        - name: bq-read-key
          mountPath: /var/secrets/bq
        env:
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: /var/secrets/bq/key.json
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: search-username-deployment-v1
spec:
  selector:
    matchLabels:
      app: search-username
      version: one
  replicas: 3
  template:
    metadata:
      labels:
        app: search-username
        version: one
    spec:
      volumes:
      - name: bq-read-key
        secret:
          secretName: bq-key
      containers:
      - name: search-username
        image: "europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchusername:latest"
        volumeMounts:
        - name: bq-read-key
          mountPath: /var/secrets/bq
        env:
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: /var/secrets/bq/key.json
```

## Update

kubectl patch deployment search-username-deployment-v1 -p "{\"spec\": {\"template\": {\"metadata\": { \"labels\": {  \"redeploy\": \"$(date +%s)\"}}}}}"
