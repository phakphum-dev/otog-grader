FROM python:3.10.19-alpine3.22 as build

WORKDIR /usr/src/app

RUN apk add --update --no-cache
# RUN rm /usr/lib/python*/EXTERNALLY-MANAGED
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN python3 -m venv /usr/src/app/venv

ENV PATH="/usr/src/app/venv/bin:$PATH"

COPY requirements.txt .

RUN apk update && apk add postgresql-dev gcc musl-dev
RUN pip3 install --requirement requirements.txt

FROM python:3.10.19-alpine3.22

WORKDIR /usr/src/app

RUN apk add --update --no-cache gcc g++

RUN apk add --update --no-cache git make libcap-dev elogind-dev asciidoc build-base

RUN apk --no-cache add libpq   

RUN git clone https://github.com/ioi/isolate.git
WORKDIR /usr/src/app/isolate
RUN git reset --hard b5e87ec10c5c83830b0ab4b9d908437e4c14e426
WORKDIR /usr/src/app

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

