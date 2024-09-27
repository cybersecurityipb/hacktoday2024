#!/bin/bash
docker compose stop forensic_legacy
docker compose rm -f forensic_legacy
docker compose up --build -d