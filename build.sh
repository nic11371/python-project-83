#!/usr/bin/env bash

make install && psql -a -d $DATABASE -f database.sql
