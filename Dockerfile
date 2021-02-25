LABEL org.opencontainers.image.source https://github.com/wahlrechner/wahlrechner

FROM python:3

RUN mkdir /code
WORKDIR /code

COPY . /code/ 
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod +x /code/docker/startup.sh
RUN chmod +x /code/docker/wait-for-it/wait-for-it.sh

RUN mkdir /static/

EXPOSE 80
