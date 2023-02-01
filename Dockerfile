FROM python:3.10
WORKDIR /viewer-app
COPY . /viewer-app/
RUN pip install --no-cache-dir Flask
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=development
RUN ["flask", "run", "--host=0.0.0.0"]