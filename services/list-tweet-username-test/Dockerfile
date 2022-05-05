# docker build . -t list-tweet-username

FROM python

RUN mkdir /service

# COPY protobufs/ /service/protobufs/
COPY . /service/list/

# ARG BIGQUERY_ACCESS_KEY
# RUN echo $BIGQUERY_ACCESS_KEY > /service/list/pythonBigQuery_credentials.json

WORKDIR /service/list
# RUN pip install -r requirements.txt

# RUN python -m grpc_tools.protoc -I ../protobufs --grpc_python_out=. \
#            ../protobufs/clear_tweet_proto.proto

# EXPOSE 50085
# ENV GOOGLE_ACCOUNT_KEY=./pythonBigQuery_credentials.json
# ENV FLASK_APP=server.py
# ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=50085"]