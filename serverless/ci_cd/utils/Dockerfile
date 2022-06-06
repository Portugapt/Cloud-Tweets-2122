FROM python:3.8.12

COPY . requirements.txt

RUN apt-get update -q update && apt-get -q install python3 python3-pip

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3" ]