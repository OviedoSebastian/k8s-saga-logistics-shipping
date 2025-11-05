# services/label-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt ./
RUN pip install -r requirements.txt

COPY app/ .

ENV SERVICE_NAME="label-service"
ENV SERVICE_PORT=5005
ENV FAILURE_RATE=0.2

EXPOSE 5005

CMD ["python", "main.py"]
