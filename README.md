# certbot-dns-hotline

[![PyPi license](https://badgen.net/pypi/license/certbot-dns-hotline/)](https://pypi.org/project/certbot-dns-hotline/) [![PyPi version](https://badgen.net/pypi/v/certbot-dns-hotline/)](https://pypi.org/project/certbot-dns-hotline/) [![PyPI Publish](https://github.com/captainGeech42/certbot-dns-hotline/workflows/PyPI%20Publish/badge.svg)](https://github.com/captainGeech42/hotline/actions?query=workflow%3A%PyPI+Publish%22) [![Docker Hub Publish](https://github.com/captainGeech42/certbot-dns-hotline/workflows/Docker%20Hub%20Publish/badge.svg)](https://github.com/captainGeech42/certbot-dns-hotline/actions?query=workflow%3A%22Docker+Hub+Publish%22) [![Docker Hub Image](https://img.shields.io/docker/v/captaingeech/certbot-dns-hotline?color=blue)](https://hub.docker.com/repository/docker/captaingeech/certbot-dns-hotline/general)

Certbot DNS plugin for Hotline

Based on https://github.com/schleuss/certbot_dns_freedns and https://github.com/m42e/certbot-dns-ispconfig

This is used in conjunction with [Hotline](https://github.com/captainGeech42/hotline) for issuing SSL certificates for the callback domain.

## Usage

Change the domains to match your callback domain, along with the `--dns-hotline-path` to the directory shared with the DNS callback service

```
$ certbot certonly \
    --authenticator dns-hotline \
    --dns-hotline-path /hotline/acme \
    --server https://acme-v02.api.letsencrypt.org/directory \
    --agree-tos \
    --rsa-key-size 4096 \
    -d 'hotlinecallback.net' \
    -d '*.hotlinecallback.net'
```