FROM python:3.10-alpine

RUN apk add --no-cache build-base gcc make tzdata
ENV TZ America/Chicago

RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "-B" , "bin/api-starter.py", "remote"]