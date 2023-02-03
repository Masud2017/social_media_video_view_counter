# FROM openstax/python3-chrome-base
# FROM ubuntu:latest

FROM mcr.microsoft.com/playwright
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10
RUN  apt install python3-pip -y
RUN  apt-get update && apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y build-essential
RUN pip3 install mysql-python

WORKDIR /app
ADD . /app

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r requirements.txt

ENV FLASK_APP=wsgi.py

# ADD xvfb_init /etc/init.d/xvfb
# RUN chmod a+x /etc/init.d/xvfb

RUN playwright install
RUN playwright install-deps


# CMD ["flask","run","-h","0.0.0.0","-p",$PORT]
CMD ["python3","wsgi.py"]