FROM openstax/python3-chrome-base

RUN  apt-get update && apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y build-essential

WORKDIR /app
ADD . /app

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r requirements.txt

ENV FLASK_APP=wsgi.py

RUN playwright install

CMD ["flask","run","-h","0.0.0.0","-p","5000"]