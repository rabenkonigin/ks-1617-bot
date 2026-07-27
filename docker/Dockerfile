FROM python:3.12.12-slim-bookworm
LABEL maintainer="yolo <justinyolo33@gmail.com>"
LABEL org.opencontainers.image.source=https://github.com/kingshot-project/Kingshot-Discord-Bot

RUN apt-get update && apt-get install --no-install-recommends -y curl ca-certificates unzip \
    && apt-get -y autoremove && apt-get -y autoclean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py version ./
COPY cogs/ ./cogs/
COPY fonts/ ./fonts/
COPY docker/bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/bin/sh", "/bootstrap.sh"]
