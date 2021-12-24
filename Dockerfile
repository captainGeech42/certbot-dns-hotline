FROM certbot/certbot

RUN mkdir /dns-hotline
WORKDIR /dns-hotline

COPY . .

RUN python setup.py install