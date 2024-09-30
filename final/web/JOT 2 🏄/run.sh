#!/bin/bash

cd $(dirname "${BASH_SOURCE[0]}")/src
fastapi run server.py
