FROM python:3.10-alpine

WORKDIR /loyalty

COPY ./loyalty_service /loyalty
COPY ../requirements.txt /loyalty

RUN pip3.10 install -r requirements.txt

EXPOSE 8050

CMD [ "python3.10", "main.py" ]
