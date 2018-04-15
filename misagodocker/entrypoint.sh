#!/usr/bin/env bash

# This file is so-called "docker entrypoint", its the script that Docker runs
# to start Misago service.

uwsgi --ini uwsgi.ini