FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r requirements.txt
RUN apk del .tmp

RUN mkdir /cars
COPY ./ /cars
WORKDIR /cars
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN adduser -D user
USER user

CMD ["entrypoint.sh"]

CMD ["python", "manage.py" "runserver"]