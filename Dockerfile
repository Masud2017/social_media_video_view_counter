FROM continuumio/anaconda3

# RUN apt-get update && apt-get install -y curl unzip

# RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
# RUN apt-get install -y nodejs

# RUN npm i -g playwright
ADD . /app
WORKDIR /app

ENTRYPOINT ["python","wsgi.py"]
