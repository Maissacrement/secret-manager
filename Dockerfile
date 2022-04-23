FROM docker

COPY requirement.txt /tmp/requirement.txt 
COPY ./app.py /usr/bin/secret-manager
COPY ./incron/ /etc
COPY ./entrypoint.sh /entrypoint
RUN mkdir -p /home/test/watcher /etc/incrond/cmd/
COPY ./cmd/update /etc/incron/cmd/
COPY ./test-file /test-file

RUN touch /var/log/test
RUN chmod +x /entrypoint /etc/incron/cmd/update
RUN apk update && apk add python3 py3-pip openrc bash incron gettext # --no-cache
RUN pip3 install -r /tmp/requirement.txt

USER root
VOLUME [ "/sys/fs/cgroup" ]
ENTRYPOINT [ "/entrypoint" ]