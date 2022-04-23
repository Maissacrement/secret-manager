#!/bin/sh
set -e
mkdir -p /run/openrc/
touch /run/openrc/softlevel
touch /var/log/test
#if [ ! 1 -eq $(alias cp &>/dev/null | wc -l) ]; then
#    alias cp='_cp() { cp $@ && /etc/incron/cmd/update ${@: -1} ;}; _cp';
#fi
echo "Service 'Incrond': Starting ..."
/usr/sbin/incrond -f /etc/incron.conf > /var/log/test &
secret-manager --template='/etc/template.watcher.yml'
tail -f /var/log/test