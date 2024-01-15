FROM python:3.10-alpine

WORKDIR /gateway

COPY ./gateway_service /gateway
COPY ../config.yaml /gateway
COPY ../requirements.txt /gateway

RUN pip3.10 install -r requirements.txt

EXPOSE 8080

CMD [ "python3.10", "main.py" ]