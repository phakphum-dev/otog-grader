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

WORKDIR /usr/src/app

RUN apk add --update --no-cache python3 gcc g++

RUN apk add --update --no-cache git make libcap-dev asciidoc

RUN git clone https://github.com/ioi/isolate.git

RUN make --directory=isolate isolate
RUN make --directory=isolate install

# RUN addgroup -S otog -g 1000 \
#     && adduser -S -G otog -u 1000 otog

#RUN chown otog:otog /usr/src/app

COPY --from=build /usr/src/app/venv ./venv

COPY . .

#USER otog

ENV PATH="/usr/src/app/venv/bin:$PATH"

CMD ["python3","-u","src/mainPostgresql.py"]

