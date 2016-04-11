FROM alpine

RUN apk add --update python python-dev py-pip && \
    pip install flask flask-sqlalchemy pymysql docker-py && \
    rm /var/cache/apk/*

ADD localtime /etc/localtime

ADD . /webapp/

EXPOSE 8080

WORKDIR /webapp

RUN chmod u+x "entry.sh"

ENTRYPOINT ["./entry.sh"]

