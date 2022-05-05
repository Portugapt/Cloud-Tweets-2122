# Execute command on ../ (this means inside services folder)
# Services folder has to contain a file called pythonBigQuery_credentials.json with google cloud access key
# docker build . -f admin-add-tweet/Dockerfile -t admin-add-tweet

FROM python

RUN mkdir /service

COPY protobufs/ /service/protobufs/
COPY admin-add-tweet/ /service/admin/

ARG BIGQUERY_ACCESS_KEY
RUN echo $BIGQUERY_ACCESS_KEY > /service/admin/pythonBigQuery_credentials.json

WORKDIR /service/admin
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
                ../protobufs/auth_proto.proto

EXPOSE 50051
ENV GOOGLE_ACCOUNT_KEY=./pythonBigQuery_credentials.json
ENV FLASK_APP=server.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=50051"]