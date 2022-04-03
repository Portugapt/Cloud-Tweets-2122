ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/minimal-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

COPY requirements.txt .
RUN pip install -r requirements.txt

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}