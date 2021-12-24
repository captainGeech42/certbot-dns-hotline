# certbot-dns-hotline
Certbot DNS plugin for Hotline

Based on https://github.com/schleuss/certbot_dns_freedns and https://github.com/m42e/certbot-dns-ispconfig

This is used in conjunction with [Hotline](https://github.com/captainGeech42/hotline) for issuing SSL certificates for the callback domain.

## Usage

Change the domains to match your callback domain, along with the `--dns-hotline-path` to the directory shared with the DNS callback service

```
$ certbot certonly \
    --authenticator dns-freedns \
    --dns-hotline-path /hotline/acme \
    --server https://acme-v02.api.letsencrypt.org/directory \
    --agree-tos \
    --rsa-key-size 4096 \
    -d 'hotlinecallback.net' \
    -d '*.hotlinecallback.net'
```