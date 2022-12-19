FROM python:3.10.6-alpine

LABEL maintainer="sergiishevchenko017@gmail.com"

RUN apk update && apk upgrade && apk add bash
WORKDIR /app
COPY . .

RUN python3 -m ensurepip
RUN python3 -m venv env
RUN source ./env/bin/activate

RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt
CMD python3 ./main.py