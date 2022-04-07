FROM python

RUN mkdir /list-tweet-username
COPY . /list-tweet-username

RUN pip install -r requirements.txt	

WORKDIR /list-tweet-username
RUN pip install -r requirements.txt
RUN python3 -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/proto.proto
#RUN openssl req -nodes -newkey rsa:4096 -subj /CN=marketplace \
#                -keyout client.key -out client.csr
#RUN --mount=type=secret,id=ca.key \
#    openssl x509 -req -in client.csr -CA ca.pem -CAkey /run/secrets/ca.key \
#                 -set_serial 1 -out client.pem

EXPOSE 5000
ENV FLASK_APP=marketplace.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]