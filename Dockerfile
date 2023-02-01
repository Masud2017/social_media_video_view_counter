FROM python:3.8
WORKDIR /viewer-app
COPY . /viewer-app/
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=development
CMD ["flask", "run", "--host=0.0.0.0"]
