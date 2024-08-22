#!/bin/bash

su postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD '${POSTGRES_PASSWORD}';\""
su postgres -c "/usr/lib/postgresql/15/bin/postgres -D /var/lib/postgresql/data &"
sleep 5
python3 app.py