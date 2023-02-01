FROM python:latest

RUN apt-get update && apt-get install -y curl unzip

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

RUN npm i -g playwright

ADD . /app
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /app

ENTRYPOINT ["flask","run"]
