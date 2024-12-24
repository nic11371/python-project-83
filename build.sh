#!/usr/bin/env bash

make install-uv && make install && psql -a -d $DATABASE_URL -f database.sql
