ARG UBUNTU_VERSION=24.04
FROM ubuntu:${UBUNTU_VER}

ARG APP_VERSION=1.0.0
ENV APP_VERSION=${APP_VERSION}

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY greet .

CMD ["./greet"]
