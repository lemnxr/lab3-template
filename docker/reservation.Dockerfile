FROM python:3.10-alpine

WORKDIR /reservation

COPY ./reservation_service /reservation
COPY ../requirements.txt /reservation

RUN pip3.10 install -r requirements.txt

EXPOSE 8070

CMD [ "python3.10", "main.py" ]
