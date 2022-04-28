# syntax = docker/dockerfile:1.0-experimental
# DOCKER_BUILDKIT=1 docker build . -f recommendations/Dockerfile -t recommendations --secret id=ca.key,src=ca.key

FROM python

RUN mkdir /service

COPY protobufs/ /service/protobufs/
COPY searchUsername/ /service/search/

WORKDIR /service/search
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
                ../protobufs/tweetMessages.proto
RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/searchUserService.proto

EXPOSE 60220
ENTRYPOINT [ "python", "searchUsername.py" ]

