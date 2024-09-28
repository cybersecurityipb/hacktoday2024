#!/bin/sh
docker build --tag=stegoscan .
docker run -it -p 1337:1337 --rm --name=stegoscan stegoscan
