#!/bin/bash
declare -i i=190

while ((i>=100))
do
  sleep 0.1
  echo volume $i | nc -q 0 127.0.0.1 8877
  let --i
done
