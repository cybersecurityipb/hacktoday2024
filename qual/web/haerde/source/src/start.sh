#!/bin/bash

su postgres -c "/usr/lib/postgresql/15/bin/postgres -D /var/lib/postgresql/data start"
su postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD '${POSTGRES_PASSWORD}';\""
sleep 5
python3 app.py