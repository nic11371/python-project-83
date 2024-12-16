#!/usr/bin/env bash

make install && psql -a -d page_analyzer -f database.sql
