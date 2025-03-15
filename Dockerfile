FROM python:3.13-slim

WORKDIR /app

RUN pip install flask pyOpenSSL

COPY ./code /app/code

EXPOSE 443

ENTRYPOINT ["python3", "/app/code/server.py"]
