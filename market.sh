#!/bin/bash

PATH=/usr/bin:$PATH
PATH=/usr/sbin:$PATH
PATH=/usr/local/bin:$PATH

cd /Users/kurebayashi/Documents/RagnarokM
while true
do
  /usr/bin/python3 /Users/kurebayashi/Documents/RagnarokM/market.py &
  sleep 3600
done
