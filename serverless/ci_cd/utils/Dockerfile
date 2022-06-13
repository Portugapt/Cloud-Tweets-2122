FROM python:3.8.12

COPY requirements.txt .
COPY requirements-pulumi.txt .

RUN apt-get -q update && apt-get -qqy install python3 python3-pip

RUN python3 -m pip install -r requirements.txt

RUN curl -fsSL https://get.pulumi.com | sh

ENTRYPOINT [ "python3" ]