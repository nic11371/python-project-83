#!/usr/bin/env bash

make poetry-install || make install && psql -a -d $DATABASE_URL -f database.sql
