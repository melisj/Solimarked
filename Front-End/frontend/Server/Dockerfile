FROM ubuntu:latest

RUN apt update -y && apt upgrade -y && apt install python3-pip -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]