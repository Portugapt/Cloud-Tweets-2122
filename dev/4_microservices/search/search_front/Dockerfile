# syntax = docker/dockerfile:1.0-experimental
# DOCKER_BUILDKIT=1 docker build . -f recommendations/Dockerfile -t recommendations --secret id=ca.key,src=ca.key

FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY search_front/ /service/search/

WORKDIR /service/search
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
                ../protobufs/tweetMessages.proto
RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/searchStringService.proto
RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/searchUserService.proto

EXPOSE 60200
ENV FLASK_APP=searchFront.py
ENV FLASK_RUN_PORT=60200
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]

