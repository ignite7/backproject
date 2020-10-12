#!/bin/sh

set -o errexit
set -o nounset

mkdir -p /ect/Caddyfile/
cp Caddyfile /etc/Caddyfile/
