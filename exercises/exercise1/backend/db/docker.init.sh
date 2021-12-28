#!/bin/bash
set -e

export PGPASSWORD=root

psql -w -U postgres <<-EOSQL
    CREATE DATABASE app;
EOSQL

psql -w -d app -U postgres < /tmp/app/install.postgres.sql
psql -w -d app -U postgres < /tmp/app/data.postgres.sql

unset PGPASSWORD