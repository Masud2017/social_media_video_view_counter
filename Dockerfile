FROM ubuntu:latest

# RUN add-apt-repository universe
RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install default-libmysqlclient-dev -y

ADD ./requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt
ADD . /opt/social-media-views-counter

WORKDIR /opt/social-media-views-counter

RUN playwright install
RUN playwright install-deps



CMD gunicorn --bind 0.0.0.0:$PORT wsgi