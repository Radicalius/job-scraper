#!/bin/bash

if [ -s "jobs.csv" ]; then
  echo "Jobs file exists; skipping scraping"
else
  python crawler.py &
fi
python dummy_server.py $PORT
