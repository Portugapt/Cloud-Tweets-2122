ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/pyspark-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root
RUN apt-get update && apt-get install -y \
curl

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-377.0.0-linux-x86_64.tar.gz

COPY requirements.txt .
RUN pip install -r requirements.txt

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}