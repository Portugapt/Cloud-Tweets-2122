# Execute command on ../
# docker build . -f admin-add-tweet/Dockerfile -t admin-add-tweet

FROM python

RUN mkdir /service

COPY protobufs/ /service/protobufs/
COPY admin-add-tweet/ /service/admin/

WORKDIR /service/admin
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
                ../protobufs/auth_proto.proto

EXPOSE 50051
ENV FLASK_APP=server.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]