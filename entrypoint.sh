#!/bin/sh

set -e

mkdir -p /run/openrc/
touch /run/openrc/softlevel
touch /var/log/test
echo "Service 'Incrond': Starting ..."
/usr/sbin/incrond -f /etc/incron.conf > /var/log/test &
/bin/bash -c "sleep 5;cp -R /test-file /home/test/watcher;" &
tail -f /var/log/test
