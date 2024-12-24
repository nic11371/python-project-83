#!/usr/bin/env bash

make uv-install && uv-env && uv-env-path && make install && psql -a -d $DATABASE_URL -f database.sql
