# Execute command on ../
# docker build . -f clear-tweet-list/Dockerfile -t clear-tweet-list

FROM python

RUN mkdir /service

COPY protobufs/ /service/protobufs/
COPY clear-tweet-list/ /service/list/

WORKDIR /service/list
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/clear_tweet_proto.proto

EXPOSE 50060
ENTRYPOINT [ "python", "server.py" ]