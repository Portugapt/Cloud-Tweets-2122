# Execute command on ../ (this means inside services folder)
# Services folder has to contain a file called pythonBigQuery_credentials.json with google cloud access key
# docker build . -f list-tweet-username/Dockerfile -t list-tweet-username

FROM python

RUN mkdir /service

COPY protobufs/ /service/protobufs/
COPY list-tweet-username/ /service/list/

WORKDIR /service/list
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
           ../protobufs/clear_tweet_proto.proto

EXPOSE 50085
ENV FLASK_APP=server.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=50085"]