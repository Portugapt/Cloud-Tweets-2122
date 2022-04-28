# lISTS Services

- [lISTS Services](#lists-services)
  - [TODO](#todo)
  - [Protobufs](#protobufs)
    - [Lists Front](#lists-front)
    - [Location](#location)
    - [Language](#language)
  - [Create, Tag and Push images](#create-tag-and-push-images)
    - [Lists Front](#lists-front-1)
  - [Services](#services)
  - [Deployments](#deployments)
  - [Update](#update)

## TODO


## Protobufs

### Lists Front

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto
            
python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/LocationListService.proto
```

### Location

For both bdLocations and cleanLocations

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto
            
python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/LocationListService.proto
```

### Language

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto
            
python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/LanguageListService.proto
```


## Create, Tag and Push images


### Lists Front

```bash
docker build . -f search_front/Dockerfile -t searchflask:3.0

docker tag searchflask:3.0 \
europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchflask:latest

docker push europe-west1-docker.pkg.dev/cadeira-nuvem-2122/cloud-microservices/searchflask:latest
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
    port: 60300
    targetPort: 60300
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
```

## Update

kubectl patch deployment search-username-deployment-v1 -p "{\"spec\": {\"template\": {\"metadata\": { \"labels\": {  \"redeploy\": \"$(date +%s)\"}}}}}"
