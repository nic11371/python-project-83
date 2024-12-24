#!/usr/bin/env bash

make uv-install && make install && psql -a -d $DATABASE_URL -f database.sql
