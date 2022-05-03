# Execute command on ../
# docker build . -f list-tweet-search/Dockerfile -t list-tweet-search

FROM python

RUN mkdir /service

COPY protobufs/ /service/protobufs/
COPY list-tweet-search/ /service/list/

WORKDIR /service/list
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/clear_tweet_proto.proto

EXPOSE 50084
ENV FLASK_APP=server.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]