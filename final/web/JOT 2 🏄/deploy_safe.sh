#!/bin/sh

docker compose down
mkdir -p ./src/databases
cp database.db ./src/databases/database.db
rm -rf ./src/__pycache__
mkdir -p ./src/__pycache__
chown -R 1000:1000 ./src/databases
chown -R 1000:1000 ./src/__pycache__
cd src
python3 db.py
cd ..
docker compose up -d --build --wait

