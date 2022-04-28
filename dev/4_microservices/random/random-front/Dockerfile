# syntax = docker/dockerfile:1.0-experimental
# DOCKER_BUILDKIT=1 docker build . -f marketplace/Dockerfile -t marketplace --secret id=ca.key,src=ca.key

FROM python

RUN mkdir /service
COPY requirements/requirements-front.txt /service/random/requirements.txt
RUN pip install -r service/random/requirements.txt

COPY protobufs/ /service/protobufs/
COPY random-front/ /service/random/

WORKDIR /service/random
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
            ../protobufs/tweetMessages.proto
            
RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/tweetLangService.proto

RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/tweetTimeService.proto

EXPOSE 60100
ENV FLASK_APP=randomtweets.py
ENV FLASK_RUN_PORT=60100
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]