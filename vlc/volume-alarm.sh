#!/bin/bash
declare -i i=100

while ((i<=190))
do
  sleep 1.5
  echo volume $i | nc -q 0 127.0.0.1 8877
  let ++i
done
