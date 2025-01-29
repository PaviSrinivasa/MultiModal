FROM python:3.10.12

ENV POSTGRES_USER mpi-multimodal-admin	
ENV POSTGRES_PASSWORD mpimultimodalad*min
ENV POSTGRES_DB mpi-multimodal

COPY init.sql /docker-entrypoint-initdb.d/