#!/bin/sh
set -e
mkdir -p /run/openrc/
touch /run/openrc/softlevel
touch /var/log/test
echo "Service 'Incrond': Starting ..."
/usr/sbin/incrond -f /etc/incron.conf > /var/log/test &
secret-manager
tail -f /var/log/test