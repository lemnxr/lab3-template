FROM python:3.10-alpine

WORKDIR /payment

COPY ./payment_service /payment
COPY ../requirements.txt /payment

RUN pip3.10 install -r requirements.txt

EXPOSE 8060

CMD [ "python3.10", "main.py" ]
