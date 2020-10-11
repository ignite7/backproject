#!/bin/sh

set -o errexit
set -o nounset

mkdir /ect/Caddyfile/
cp Caddyfile /etc/Caddyfile
