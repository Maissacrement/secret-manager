FROM alpine

COPY ./incron/ /etc
COPY ./entrypoint.sh /entrypoint
RUN mkdir -p /home/test/watcher /etc/incrond/cmd/
COPY ./cmd/update /etc/incron/cmd/
COPY ./provision /provision

RUN chmod +x /entrypoint /etc/incron/cmd/update
RUN apk update && apk add --no-cache incron gettext
ENTRYPOINT ["/entrypoint"]