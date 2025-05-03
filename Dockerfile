FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV DB_HOST=db
ENV DB_NAME=mydb
ENV DB_USER=user
ENV DB_PASSWORD=password

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]