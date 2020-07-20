FROM python:3.8-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
RUN apk update && apk add --no-cache --virtual .build-deps libffi libffi-dev musl musl-dev gcc

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --prefix /install -r /requirements.txt


FROM base
COPY --from=builder /install /usr/local
COPY file_server/ /app/file_server/
WORKDIR /app

EXPOSE 80
CMD python3 -m file_server -H 0.0.0.0 -P 80
