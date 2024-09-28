#!/bin/sh
docker build --tag=stegoscan .
docker run -itd -p 1337:1337 --rm --name=stegoscan stegoscan
