FROM python:3.8-alpine

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r requirements.txt

RUN mkdir /app
COPY ./ /app
WORKDIR /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]