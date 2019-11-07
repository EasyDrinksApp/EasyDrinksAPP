FROM alpine:3.10

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip \
    && apk --no-cache add build-base \
    && apk --no-cache add postgresql-dev

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

CMD [ "python3.7", "src/App.py" ]