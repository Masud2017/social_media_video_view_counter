FROM mcr.microsoft.com/playwright
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]