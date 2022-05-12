# Execute command on ../ (this means inside services folder)
# Services folder has to contain a file called pythonBigQuery_credentials.json with google cloud access key
# docker build . -f admin-delete-tweet/Dockerfile -t admin-delete-tweet

FROM python

RUN mkdir /service

COPY protobufs/ /service/protobufs/
COPY admin-delete-tweet/ /service/admin/

WORKDIR /service/admin
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
                ../protobufs/auth_proto.proto

EXPOSE 50052
ENV FLASK_APP=server.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=50052"]