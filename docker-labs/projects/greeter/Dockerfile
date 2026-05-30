FROM ubuntu:24.04

WORKDIR /app

COPY greet .

RUN chmod +x greet

ENV GREETING=Hiya
ENV NAME=Partner

CMD ["./greet"]

