#!/bin/bash

docker-compose up -d
python trackerdcs/sensors/dht11.py localhost test_dht11 &

