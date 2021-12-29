FROM alpine:3.15 as build

WORKDIR /usr/src/app

RUN apk add --update --no-cache python3
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN python3 -m venv /usr/src/app/venv

ENV PATH="/usr/src/app/venv/bin:$PATH"

COPY requirements.txt .

RUN pip3 install --requirement requirements.txt

FROM alpine:3.15

RUN apk add --update --no-cache python3 gcc g++

RUN addgroup -S otog -g 1000 \
    && adduser -S -G otog -u 1000 otog

USER otog

WORKDIR /usr/src/app

COPY --chown=otog:otog --from=build /usr/src/app/venv ./venv
COPY --chown=otog:otog config.ini ./
COPY --chown=otog:otog src/ ./src

ENV PATH="/usr/src/app/venv/bin:$PATH"

CMD ["python3","-u","src/main.py"]
