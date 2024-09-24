#!/bin/sh

mosquitto_sub -h slateplus.lan  -u "gasread" -P "Hello" -v -t "sensors/gas/#" --qos 1 --id "gasread" --disable-clean-session |
while read payload; do
  echo Received $payload | tee /root/gas_data.csv
done
