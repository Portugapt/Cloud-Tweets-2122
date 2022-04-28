# syntax = docker/dockerfile:1.0-experimental
# DOCKER_BUILDKIT=1 docker build . -f recommendations/Dockerfile -t recommendations --secret id=ca.key,src=ca.key

FROM python

RUN mkdir /service

COPY requirements/requirements-back.txt /service/random/requirements.txt
RUN pip install -r service/random/requirements.txt

COPY protobufs/ /service/protobufs/
COPY random-timeinterval/ /service/random/

WORKDIR /service/random

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
                ../protobufs/tweetMessages.proto
RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/tweetTimeService.proto

EXPOSE 60120
ENTRYPOINT [ "python", "randomTime.py" ]

