#!/usr/bin/env bash

pip install -r requirements.txt || make install && psql -a -d $DATABASE_URL -f database.sql
