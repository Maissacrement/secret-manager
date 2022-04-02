FROM docker

COPY ./incron/ /etc
COPY ./entrypoint.sh /entrypoint
RUN mkdir -p /home/test/watcher /etc/incrond/cmd/
COPY ./cmd/update /etc/incron/cmd/
COPY ./test-file /test-file

RUN touch /var/log/test
RUN chmod +x /entrypoint /etc/incron/cmd/update
RUN apk update && apk add --no-cache openrc bash incron gettext

USER root
VOLUME [ "/sys/fs/cgroup" ]
ENTRYPOINT [ "/entrypoint" ]