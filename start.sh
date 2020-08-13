#!/bin/bash

python crawler.py &
python dummy_server.py $PORT
