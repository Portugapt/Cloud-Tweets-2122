# Execute command on ../ (this means inside services folder)
# docker build . -f auth/Dockerfile -t auth

FROM python

RUN mkdir /service

COPY protobufs/ /service/protobufs/
COPY auth/ /service/auth/

WORKDIR /service/auth
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
                ../protobufs/auth_proto.proto

EXPOSE 50000
ENTRYPOINT [ "python", "server.py"]